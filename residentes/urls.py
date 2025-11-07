from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import api_views # importa las nuevas vistas api


urlpatterns = [
    path('', views.index, name='index'),
    path('login1/', views.login1, name='login1'),
    path('register/', views.register, name='register'),
    path('usuario/', views.usuario, name='usuario'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('usuario_dashboard/', views.usuario_dashboard, name='usuario_dashboard'), 
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Vista de administrador
    path('operador_dashboard/', views.operador_dashboard, name='operador_dashboard'),  # Vista de operador
    path('buscar_documentos/', views.buscar_documentos, name='buscar_documentos'),
    path('subir_documento/', views.subir_documento, name='subir_documento'),
    path('login_por_sensor/', views.login_por_sensor, name='login_por_sensor'),
 #  path('api/recibir_huella/', views.recibir_huella, name='recibir_huella'),
# Endpoint de status (ping)
    path('api/fingerprint/status/', api_views.fingerprint_status, name='api_fingerprint_status'),
    
    # Endpoint para verificar si una huella existe
    path('api/fingerprint/verify/', api_views.fingerprint_verify, name='api_fingerprint_verify'),
    
    # Endpoint principal para login con huella
    path('api/fingerprint/login/', api_views.fingerprint_login, name='api_fingerprint_login'),
    
    # Endpoint legacy (compatibilidad con código anterior)
    path('api/fingerprint/legacy/', api_views.fingerprint_legacy, name='api_fingerprint_legacy'),
]




