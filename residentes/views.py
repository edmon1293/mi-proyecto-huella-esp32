from django.shortcuts import render, redirect
import requests
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Usuario, Domicilio, Contacto
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from .models import Documento  # Asegúrate de importar tu modelo correcto
from .forms import BusquedaForm
from .forms import DocumentoForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Usuario

# CONFIGURACIÓN CRÍTICA
# *****************************************************************
# 🚨 ¡IMPORTANTE! Reemplaza esto con la IP estática o reservada de tu ESP32.
# Si el ESP32 cambia de IP, esta vista fallará.
ESP32_IP = "192.168.1.18" # Ejemplo: ajusta esta IP
# *****************************************************************

@csrf_exempt
def recibir_huella(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        huella_id = data.get('huella_id')

        if huella_id is None:
            return JsonResponse({'error': 'No se recibió huella_id'}, status=400)

        try:
            usuario = Usuario.objects.get(sensor_id=huella_id)
            if usuario.is_active:
                return JsonResponse({'acceso': 'permitido', 'rol': usuario.rol})
            else:
                return JsonResponse({'acceso': 'denegado', 'motivo': 'usuario inactivo'}, status=403)
        except Usuario.DoesNotExist:
            return JsonResponse({'acceso': 'denegado', 'motivo': 'ID no registrado'}, status=404)

    return JsonResponse({'error': 'Método no permitido'}, status=405)



def login_por_sensor(request):
    """
    Función de vista que inicia la verificación de huella en el ESP32
    y autentica al usuario en Django si el ID es reconocido (incluyendo el ID 0 del administrador).
    """
    # IP del ESP32 (Asegúrate de que coincida con la IP actual del ESP32)
    ESP32_IP = "192.168.1.18" 

    # Tiempo de espera en segundos. Debe ser MAYOR que el tiempo de espera del ESP32 (5s).
    TIMEOUT_SECONDS = 6 

    try:
        # 1. Enviar solicitud al ESP32 para iniciar la verificación
        url_verificar = f"http://{ESP32_IP}/verificar"
        
        print(f"DEBUG: Enviando solicitud a ESP32 en {url_verificar} para verificar huella (Timeout: {TIMEOUT_SECONDS}s).")
        
        # Aumentamos el timeout para dar margen, ahora que el ESP32 responde en 5s.
        response = requests.get(url_verificar, timeout=TIMEOUT_SECONDS)
        
        # 2. Procesar la respuesta del ESP32
        if response.status_code != 200:
            return HttpResponse(f"Error al comunicar con ESP32. Código HTTP: {response.status_code}", status=500)

        # La respuesta esperada es un ID numérico (ej: "0", "5")
        sensor_id_str = response.text.strip()
        user_id = int(sensor_id_str)
        
        # CRÍTICO: Solo se bloquea si el ID es NEGATIVO. 
        # Si user_id es 0 (Admin) o positivo, continúa la autenticación.
        if user_id < 0:
             return HttpResponse("⛔ ID de sensor no reconocido o inválido.", status=404)

        # Si user_id es 0, significa que el ESP32 agotó el tiempo O que encontró al Admin (ID 0).
        if user_id == 0:
            # Ahora necesitamos verificar si fue por timeout o si fue el administrador.
            # En nuestro caso, si se agotó el tiempo en el ESP32, el ESP32 envía 0.
            # Si el usuario es ID 0, procederá a la autenticación (punto 3).
            
            # Si el ESP32 devuelve 0 Y no existe el usuario 0, significa timeout o huella no encontrada.
            # Pero dado que el Admin tiene ID 0, intentamos la autenticación:
            pass
        
        # 3. Autenticar al usuario en Django usando el ID
        usuario = Usuario.objects.get(sensor_id=user_id)
        
        if usuario.is_active:
            # Autenticación exitosa
            login(request, usuario)
            
            # Redirección según el rol
            if usuario.rol == 3: # Rol de Administrador
                return redirect('/admin/')
            elif usuario.rol == 2: # Rol de Operador
                return redirect('operador_dashboard')
            elif usuario.rol == 1: # Rol de Usuario Estándar
                return redirect('usuario')
            else:
                return redirect('index') # Redirección por defecto
        else:
            return HttpResponse("Usuario inactivo", status=403)

    except requests.exceptions.Timeout:
        return HttpResponse(f"Tiempo de conexión con ESP32 agotado (Timeout en {TIMEOUT_SECONDS}s).", status=504)

    except requests.exceptions.ConnectionError:
        return HttpResponse("ESP32 no está en línea o la IP es incorrecta (Error de conexión de red).", status=503)

    except Usuario.DoesNotExist:
        # Aquí caerá si:
        # 1. El ID de sensor encontrado (user_id) no está en la base de datos.
        # 2. El ESP32 devolvió 0 (Timeout) Y NO existe un usuario con sensor_id=0. 
        #    Si existe el Admin (ID 0), esto no ocurrirá para el caso de Admin.
        if user_id == 0:
             return HttpResponse("⛔ Tiempo agotado en la espera de huella o el administrador no existe.", status=404)
        else:
             return HttpResponse(f"⛔ Huella con ID ({user_id}) no registrada en el sistema.", status=404)

    except Exception as e:
        # Captura cualquier otro error
        return HttpResponse(f"⚠️ Error inesperado en Django: {str(e)}", status=500)



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirecciona según el rol del usuario
            if user.rol == 3:
                return redirect('/admin/')  # Suponiendo que rol 3 es de administrador
            elif user.rol == 2:
                return redirect('operador_dashboard')
            elif user.rol == 1:
                return redirect('usuario_dashboard')  # Suponiendo que rol 1 es de usuario normal
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Crear y guardar el domicilio
            domicilio = Domicilio(
                calle=form.cleaned_data['calle'],
                numero_exterior=form.cleaned_data['numero_exterior'],
                colonia=form.cleaned_data['colonia'],
                municipio=form.cleaned_data['municipio'],
                cp=form.cleaned_data['cp'],
                ciudad=form.cleaned_data['ciudad']
            )
            domicilio.save()

            # Crear y guardar el usuario
            user = Usuario(
                email=form.cleaned_data['email'],
                nombre=form.cleaned_data['nombre'],
                apellidos=form.cleaned_data['apellidos'],
                edad=form.cleaned_data['edad'],
                universidad=form.cleaned_data['universidad'],
                carrera=form.cleaned_data['carrera'],
                ID_domicilio=domicilio,
                rol=1,  # Por defecto el rol puede ser 2
                is_active=True,
                is_staff=False,
                INE=form.cleaned_data['INE'],
                CURP=form.cleaned_data['CURP'],
                COMPROBANTE_DOMICILIO=form.cleaned_data['COMPROBANTE_DOMICILIO'],
                ACTA_NACIMIENTO=form.cleaned_data['ACTA_NACIMIENTO'],
                CONSTANCIA_DERECHOS=form.cleaned_data['CONSTANCIA_DERECHOS'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Crear y guardar el contacto
            contacto = Contacto(
                ID_usuario=user,
                contacto=form.cleaned_data['contacto'],
                tipo=form.cleaned_data['tipo']
            )
            contacto.save()

            # Iniciar sesión y redirigir al usuario
            login(request, user)
            return redirect('login1')  # Cambia a 'usuario'
    else:
        form = RegisterForm()
    return render(request, 'residentes/register.html', {'form': form})

def superuser_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = True
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('admin:index')  # Redirige al panel de administración
    else:
        form = UserCreationForm()
    return render(request, 'residentes/superuser_register.html', {'form': form})
@login_required
def operador_dashboard(request):
    # Asegúrate de que el usuario tenga el rol de operador
    if request.user.rol != 2:  # Suponiendo que el rol 2 es de operador
        return redirect('home')  # Redirige a la página principal o a otra página de error

    # Lógica para buscar documentos u otras funcionalidades para operadores
    return render(request, 'operador_dashboard.html')

@login_required
def buscar_documentos(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        # Implementa la lógica de búsqueda según tu modelo
        documentos = Documentos.objects.filter(nombre__icontains=query)
        return render(request, 'resultados_busqueda.html', {'documentos': documentos})

def index(request):
    return render(request, 'residentes/index.html')

def login1(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.rol == 3:
                return redirect('/admin/')
            elif user.rol == 2:
                return redirect('operador_dashboard')
            elif user.rol == 1:
                return redirect('usuario')
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'residentes/login1.html', {'form': form})

def usuario(request):
    user = request.user
    return render(request, 'residentes/usuario.html', {
        'user': user,
        'domicilio': user.ID_domicilio,
        'contacto': Contacto.objects.filter(ID_usuario=user).first()  # Tomar el primer contacto asociado
    })

def buscar_documentos(request):
    query = request.GET.get('q', '')  # Obtén el valor de 'q' de la solicitud GET
    if query:
        documentos = Documento.objects.filter(nombre__icontains=query)  # Filtra los documentos
    else:
        documentos = Documento.objects.all()  # Si no hay búsqueda, muestra todos los documentos
    
    return render(request, 'buscador.html', {'documentos': documentos})

def subir_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subir_documento')  # Redirige a la misma página después de subir
    else:
        form = DocumentoForm()
    
    return render(request, 'subir_documento.html', {'form': form})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def operador_dashboard(request):
    return render(request, 'operador_dashboard.html')

@login_required
def usuario_dashboard(request):
    return render(request, 'usuario_dashboard.html')
def es_operador(user):
    return user.rol == 2

def es_administrador(user):
    return user.rol == 3

@login_required
@user_passes_test(es_operador)
def operador_dashboard(request):
    return render(request, 'operador_dashboard.html')

@login_required
@user_passes_test(es_administrador)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')