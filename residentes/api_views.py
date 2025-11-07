from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login
from .models import Usuario
import json


@csrf_exempt
@require_http_methods(["GET"])
def fingerprint_status(request):
    """
    Endpoint para verificar que el servicio está funcionando.
    El ESP32 puede usar esto para hacer un "ping" inicial.
    """
    return JsonResponse({
        'status': 'online',
        'service': 'fingerprint-auth',
        'version': '1.0',
        'message': 'Sistema de autenticación por huella activo'
    })


@csrf_exempt
@require_http_methods(["POST"])
def fingerprint_verify(request):
    """
    Verifica si una huella existe en el sistema (sin hacer login).
    Útil para testing desde el ESP32.
    
    Espera JSON: {"sensor_id": 123}
    """
    try:
        data = json.loads(request.body)
        sensor_id = data.get('sensor_id')
        
        if sensor_id is None:
            return JsonResponse({
                'success': False,
                'error': 'sensor_id es requerido'
            }, status=400)
        
        # Verificar si existe el usuario con ese sensor_id
        exists = Usuario.objects.filter(sensor_id=sensor_id, is_active=True).exists()
        
        if exists:
            usuario = Usuario.objects.get(sensor_id=sensor_id)
            return JsonResponse({
                'success': True,
                'exists': True,
                'sensor_id': sensor_id,
                'rol': usuario.rol,
                'nombre': usuario.nombre
            })
        else:
            return JsonResponse({
                'success': True,
                'exists': False,
                'sensor_id': sensor_id,
                'message': 'Huella no registrada'
            })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def fingerprint_login(request):
    """
    Endpoint para autenticación por huella desde ESP32.
    Este endpoint hace login en Django y retorna la información del usuario.
    
    Espera JSON: 
    {
        "sensor_id": 123,
        "device_id": "ESP32_001" (opcional)
    }
    """
    try:
        # Parsear datos del ESP32
        data = json.loads(request.body)
        sensor_id = data.get('sensor_id')
        device_id = data.get('device_id', 'unknown')
        
        # Validar datos
        if sensor_id is None:
            return JsonResponse({
                'success': False,
                'error': 'sensor_id es requerido'
            }, status=400)
        
        # Buscar usuario por sensor_id
        try:
            usuario = Usuario.objects.get(sensor_id=sensor_id)
            
            # Verificar que el usuario esté activo
            if not usuario.is_active:
                return JsonResponse({
                    'success': False,
                    'error': 'Usuario inactivo',
                    'sensor_id': sensor_id
                }, status=403)
            
            # Autenticar (login) al usuario en Django
            # Nota: Utilizamos el backend ModelBackend por defecto
            login(request, usuario, backend='django.contrib.auth.backends.ModelBackend')
            
            # Mapear rol a nombre legible
            rol_nombres = {
                1: 'Usuario',
                2: 'Operador',
                3: 'Administrador'
            }
            
            # Retornar información del usuario
            return JsonResponse({
                'success': True,
                'message': 'Autenticación exitosa',
                'user': {
                    'id': usuario.ID_usuario,
                    'email': usuario.email,
                    'nombre': usuario.nombre,
                    'apellidos': usuario.apellidos,
                    'rol': usuario.rol,
                    'rol_nombre': rol_nombres.get(usuario.rol, 'Desconocido')
                }
            })
            
        except Usuario.DoesNotExist:
            # Huella no registrada
            return JsonResponse({
                'success': False,
                'error': 'Huella no registrada en el sistema',
                'sensor_id': sensor_id
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
        
    except Exception as e:
        # Error inesperado
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def fingerprint_legacy(request):
    """
    Endpoint legacy compatible con tu función 'recibir_huella' original.
    Mantiene compatibilidad con código existente.
    
    Espera JSON: {"huella_id": 123}
    """
    try:
        data = json.loads(request.body)
        huella_id = data.get('huella_id')

        if huella_id is None:
            return JsonResponse({'error': 'No se recibió huella_id'}, status=400)

        try:
            usuario = Usuario.objects.get(sensor_id=huella_id)
            if usuario.is_active:
                # Simula la respuesta original
                return JsonResponse({
                    'acceso': 'permitido',
                    'rol': usuario.rol,
                    'nombre': usuario.nombre
                })
            else:
                return JsonResponse({
                    'acceso': 'denegado',
                    'motivo': 'usuario inactivo'
                }, status=403)
        except Usuario.DoesNotExist:
            return JsonResponse({
                'acceso': 'denegado',
                'motivo': 'ID no registrado'
            }, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)