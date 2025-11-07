from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('administrador/', views.custom_admin, name='administrador'),
    path('formulario/', views.formulario, name='formulario'),
    path('login1/', views.login1, name='login1'),
    path('usuario/', views.usuario, name='usuario'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    # Añade más URLs según sea necesario
]
