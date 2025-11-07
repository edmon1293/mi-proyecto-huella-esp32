from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import RegisterForm, DocumentoForm
from .models import Usuario, Domicilio, Contacto, Documento


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.rol == 3:
                return redirect('/admin/')
            elif user.rol == 2:
                return redirect('operador_dashboard')
            elif user.rol == 1:
                return redirect('usuario_dashboard')
            else:
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
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

            login(request, user)
            return redirect('login1')
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
            return redirect('admin:index')
    else:
        form = UserCreationForm()
    return render(request, 'residentes/superuser_register.html', {'form': form})


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
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'residentes/login1.html', {'form': form})


@login_required
def usuario(request):
    user = request.user
    return render(request, 'residentes/usuario.html', {
        'user': user,
        'domicilio': user.ID_domicilio,
        'contacto': Contacto.objects.filter(ID_usuario=user).first()
    })


def buscar_documentos(request):
    query = request.GET.get('q', '')
    if query:
        documentos = Documento.objects.filter(nombre__icontains=query)
    else:
        documentos = Documento.objects.all()
    return render(request, 'buscador.html', {'documentos': documentos})


def subir_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('subir_documento')
    else:
        form = DocumentoForm()
    return render(request, 'subir_documento.html', {'form': form})


@login_required
def admin_dashboard(request):
    if request.user.rol != 3:
        return redirect('index')
    return render(request, 'admin_dashboard.html')


@login_required
def operador_dashboard(request):
    if request.user.rol != 2:
        return redirect('index')
    return render(request, 'operador_dashboard.html')


@login_required
def usuario_dashboard(request):
    return render(request, 'usuario_dashboard.html')


# Funciones auxiliares para verificar roles
def es_operador(user):
    return user.rol == 2


def es_administrador(user):
    return user.rol == 3