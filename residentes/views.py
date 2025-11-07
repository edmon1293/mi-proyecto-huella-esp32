from django.shortcuts import render, redirect
import requests
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, DocumentoForm
from .models import Usuario, Domicilio, Contacto, Documento 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# --- FUNCIONES AUXILIARES DE ROL ---
def es_operador(user):
    # Asegúrate de que el modelo Usuario tenga el atributo 'rol'
    return user.rol == 2 

def es_administrador(user):
    return user.rol == 3

# --- CONFIGURACIÓN CRÍTICA DEL ESP32 ---
# 🚨 ¡IMPORTANTE! Reemplaza esto con la IP estática o reservada de tu ESP32.
ESP32_IP = "192.168.1.100" # Ejemplo: ajusta esta IP

# ----------------------------------------------------------------------
# 1. VISTAS RELACIONADAS CON EL LOGIN Y REGISTRO
# ----------------------------------------------------------------------

# NOTE: Asumo que solo usarás login1, pero mantengo la estructura completa.
def login1(request):
    """ Login alternativo por credenciales. """
    if request.method == 'POST':
        # Se usa request, data para que el formulario pueda validar la sesión
        form = AuthenticationForm(request, data=request.POST) 
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # 🔑 CORRECCIÓN CLAVE: Redirigir Superusuario al panel nativo
            if user.is_superuser:
                # Usamos el nombre de URL nativo de Django Admin
                return redirect('admin:index') 
                
            # Redireccionar según el rol (para usuarios rol 3 que NO son superuser)
            elif user.rol == 3:
                return redirect('admin_dashboard')
            elif user.rol == 2:
                return redirect('operador_dashboard')
            elif user.rol == 1:
                return redirect('usuario_dashboard')
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
        
    # CORRECCIÓN DE RUTA DE PLANTILLA
    return render(request, 'residentes/login1.html', {'form': form})

def register(request):
    """ Registro de un nuevo usuario con datos de domicilio y contacto. """
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # ... (Lógica de guardado de Domicilio, Usuario y Contacto)
            domicilio = Domicilio(
                calle=form.cleaned_data['calle'],
                numero_exterior=form.cleaned_data['numero_exterior'],
                colonia=form.cleaned_data['colonia'],
                municipio=form.cleaned_data['municipio'],
                cp=form.cleaned_data['cp'],
                ciudad=form.cleaned_data['ciudad']
            )
            domicilio.save()

            user = Usuario(
                email=form.cleaned_data['email'],
                nombre=form.cleaned_data['nombre'],
                apellidos=form.cleaned_data['apellidos'],
                edad=form.cleaned_data['edad'],
                universidad=form.cleaned_data['universidad'],
                carrera=form.cleaned_data['carrera'],
                ID_domicilio=domicilio,
                rol=1,
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

            contacto = Contacto(
                ID_usuario=user,
                contacto=form.cleaned_data['contacto'],
                tipo=form.cleaned_data['tipo']
            )
            contacto.save()
            # Iniciar sesión y redirigir
            login(request, user)
            return redirect('usuario_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'residentes/register.html', {'form': form})

def superuser_register(request):
    """ Registro de superusuario (usado solo en desarrollo/setup). """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_superuser = True
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('admin:index')
    else:
        form = UserCreationForm()
    return render(request, 'residentes/superuser_register.html', {'form': form})

# ----------------------------------------------------------------------
# 2. DASHBOARDS Y VISTAS DE USUARIO
# ----------------------------------------------------------------------

def index(request):
    """ Vista principal (home). """
    return render(request, 'residentes/index.html')

@login_required
def usuario(request):
    """ Panel de usuario estándar con sus datos. """
    user = request.user
    return render(request, 'residentes/usuario.html', {
        'user': user,
        'domicilio': user.ID_domicilio,
        'contacto': Contacto.objects.filter(ID_usuario=user).first()
    })

@login_required
def usuario_dashboard(request):
    """ Dashboard del rol 1 (Usuario estándar). """
    # 🔑 CORRECCIÓN DE RUTA DE PLANTILLA
    return render(request, 'residentes/usuario_dashboard.html')

@login_required
@user_passes_test(es_operador)
def operador_dashboard(request):
    """ Dashboard del rol 2 (Operador). Requiere rol=2. """
    # 🔑 CORRECCIÓN DE RUTA DE PLANTILLA
    return render(request, 'residentes/operador_dashboard.html')

@login_required
@user_passes_test(es_administrador)
def admin_dashboard(request):
    """ Dashboard del rol 3 (Administrador). Requiere rol=3. """
    # 🔑 CORRECCIÓN DE RUTA DE PLANTILLA (Asumimos que el custom admin está aquí)
    return render(request, 'residentes/admin_dashboard.html')

# ----------------------------------------------------------------------
# 3. VISTAS DE DOCUMENTOS
# ----------------------------------------------------------------------

def buscar_documentos(request):
    """ Vista de búsqueda de documentos. """
    query = request.GET.get('q', '')
    if query:
        # Asegúrate de que 'nombre' es el campo correcto para la búsqueda
        documentos = Documento.objects.filter(nombre__icontains=query) 
    else:
        documentos = Documento.objects.all()
    
    # 🔑 CORRECCIÓN DE RUTA DE PLANTILLA
    return render(request, 'residentes/buscador.html', {'documentos': documentos})

def subir_documento(request):
    """ Vista para subir documentos usando un formulario. """
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subir_documento')
    else:
        form = DocumentoForm()
    
    # 🔑 CORRECCIÓN DE RUTA DE PLANTILLA
    return render(request, 'residentes/subir_documento.html', {'form': form})

# ----------------------------------------------------------------------
# 4. VISTA DE LOGIN POR SENSOR (PELIGROSA EN RENDER)
# ----------------------------------------------------------------------

def login_por_sensor(request):
    """
    Función de vista que intenta comunicarse con el ESP32.
    """
    try:
        url_verificar = f"http://{ESP32_IP}/verificar"
        print(f"DEBUG: Enviando solicitud a ESP32 en {url_verificar}...")
        
        response = requests.get(url_verificar, timeout=15)
        
        if response.status_code != 200:
            return HttpResponse(f"Error al comunicar con ESP32. Código: {response.status_code}", status=500)

        sensor_id_str = response.text.strip()
        user_id = int(sensor_id_str)
        
        if user_id <= 0:
             return HttpResponse("⛔ ID de sensor no reconocido o tiempo agotado.", status=404)

        usuario = Usuario.objects.get(sensor_id=user_id)
        
        if usuario.is_active:
            login(request, usuario)
            
            # 🔑 CORRECCIÓN CLAVE: Redirigir Superusuario al panel nativo
            if usuario.is_superuser:
                return redirect('admin:index')
                
            elif usuario.rol == 3:
                return redirect('admin_dashboard')
            elif usuario.rol == 2:
                return redirect('operador_dashboard')
            elif usuario.rol == 1:
                return redirect('usuario_dashboard')
            else:
                return redirect('index')
        else:
            return HttpResponse("Usuario inactivo", status=403)

    except requests.exceptions.Timeout:
        return HttpResponse("Tiempo de conexión con ESP32 agotado.", status=504)
    except requests.exceptions.ConnectionError:
        return HttpResponse("ESP32 no está en línea o la IP es incorrecta.", status=503)
    except Usuario.DoesNotExist:
        return HttpResponse(f"⛔ Huella con ID ({user_id}) no registrada.", status=404)
    except Exception as e:
        return HttpResponse(f"⚠️ Error inesperado en Django: {str(e)}", status=500)