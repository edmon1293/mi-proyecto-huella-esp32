from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import api_views  # Importar las nuevas vistas API

urlpatterns = [
    # Rutas de interfaz web
    path('', views.index, name='index'),
    path('login1/', views.login1, name='login1'),
    path('register/', views.register, name='register'),
    path('usuario/', views.usuario, name='usuario'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('usuario_dashboard/', views.usuario_dashboard, name='usuario_dashboard'), 
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('operador_dashboard/', views.operador_dashboard, name='operador_dashboard'),
    path('buscar_documentos/', views.buscar_documentos, name='buscar_documentos'),
    path('subir_documento/', views.subir_documento, name='subir_documento'),
    
    # ========== RUTAS API PARA ESP32 ==========
    # Endpoint de status (ping)
    path('api/fingerprint/status/', api_views.fingerprint_status, name='api_fingerprint_status'),
    
    # Endpoint para verificar si una huella existe
    path('api/fingerprint/verify/', api_views.fingerprint_verify, name='api_fingerprint_verify'),
    
    # Endpoint principal para login con huella
    path('api/fingerprint/login/', api_views.fingerprint_login, name='api_fingerprint_login'),
    
    # Endpoint legacy (compatibilidad)
    path('api/fingerprint/legacy/', api_views.fingerprint_legacy, name='api_fingerprint_legacy'),
]



