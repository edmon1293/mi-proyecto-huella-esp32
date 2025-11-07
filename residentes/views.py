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
import json
import logging

logger = logging.getLogger(__name__)

 #CONFIGURACIÓN CRÍTICA DEL TOKEN Y EL NUEVO ENDPOINT API
# ----------------------------------------------------------------------------------

# CRÍTICO: Debe coincidir con el token en el código del ESP32
# ⚠️ IMPORTANTE: REEMPLAZA ESTO CON UN VALOR REAL Y SEGURO (MÍNIMO 20 CARACTERES) ⚠️
AUTH_TOKEN = "c8fE2p_LzW4qXy7R_hT1jV9aB0kS3mG" 

@csrf_exempt
def recibir_huella_y_login(request):
    """
    NUEVO ENDPOINT API: Recibe el POST del ESP32 con el sensor_id y el token.
    Este endpoint verifica la autenticidad del ESP32 y si el ID existe.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sensor_id = data.get('sensor_id')
            token = data.get('token')
            # Capturamos el ID del dispositivo (MAC Address) que el ESP32 está enviando
            device_id = data.get('device_id', 'N/A') 
            
            # 1. Verificación de Seguridad (Token)
            if token != AUTH_TOKEN:
                logger.warning(f"Intento de acceso no autorizado con token: {token}")
                return JsonResponse({"success": False, "message": "Token de dispositivo inválido"}, status=401)
            
            # 2. Validación de ID (sensor_id)
            if sensor_id is None or not isinstance(sensor_id, int) or sensor_id < 1: # Si es 0 o menor, es error/timeout
                logger.error(f"ID de sensor inválido o de timeout recibido: {sensor_id}")
                return JsonResponse({"success": False, "message": "ID de sensor no válido o no encontrado"}, status=400)

            # 3. Búsqueda de Usuario
            try:
                user = Usuario.objects.get(sensor_id=sensor_id)
                
                logger.info(f"Huella verificada para el usuario: {user.email} (ID: {user.sensor_id})")
                
                # Devuelve éxito. El login de sesión en el navegador se hará por un método alternativo
                # (o si se usa un WebSocket/Polling en el futuro). Por ahora, solo confirmamos la huella.
                return JsonResponse({
                    "success": True, 
                    "message": "Huella verificada con éxito", 
                    "sensor_id": sensor_id,
                    "user_id": user.id,
                    "nombre": user.nombre
                })
                
            except Usuario.DoesNotExist:
                logger.warning(f"Huella no encontrada en la base de datos para ID: {sensor_id}")
                return JsonResponse({"success": False, "message": "Huella no registrada"}, status=404)
            
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Formato JSON inválido"}, status=400)
        except Exception as e:
            logger.error(f"Error interno en la vista: {e}", exc_info=True)
            return JsonResponse({"success": False, "message": "Error interno del servidor"}, status=500)
            
    return JsonResponse({"success": False, "message": "Método no permitido"}, status=405)


# Función que el USUARIO visitará en el navegador
def fingerprint_login_client(request):
    """
    Vista que el usuario abre en el navegador y le pide poner el dedo.
    
    NOTA: La redirección automática a /admin/ o /operador/ es compleja
    sin WebSockets. Por ahora, solo muestra el mensaje.
    """
    if request.user.is_authenticated:
        return redirect('index') 

    # Aquí deberías renderizar una plantilla que diga: "Ponga el dedo en el sensor."
    return render(request, 'residentes/esperando_huella.html', {'message': 'Por favor, ponga su dedo en el sensor biométrico.'})



# ----------------------------------------------------------------------------------
# FUNCIONES OBSOLETAS O ANTERIORES
# ----------------------------------------------------------------------------------

# La función login_por_sensor ha sido ELIMINADA por ser obsoleta en el ambiente Render.
# La función recibir_huella ha sido REEMPLAZADA por recibir_huella_y_login para mejor claridad.

# Funciones antiguas (mantener por si tienen dependencias en urls.py o templates)
def recibir_huella(request):
    # Función obsoleta, redirigida a la nueva API (mantener para evitar errores 500 si la ruta existe)
    return recibir_huella_y_login(request)


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