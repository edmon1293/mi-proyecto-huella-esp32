from django.shortcuts import render

def index(request):
    return render(request, 'residentes/index.html')

def administrador(request):
    return render(request, 'residentes/administrador.html')

def formulario(request):
    return render(request, 'residentes/formulario.html')

def login1(request):
    return render(request, 'residentes/login1.html')

def usuario(request):
    return render(request, 'residentes/usuario.html')

def custom_admin(request):
    return render(request, 'residentes/administrador.html')

