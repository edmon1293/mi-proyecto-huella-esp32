from django.core.management.base import BaseCommand
from residentes.models import Usuario, Domicilio


class Command(BaseCommand):
    help = 'Crea datos iniciales: superusuario y usuario de prueba con huella'

    def handle(self, *args, **kwargs):
        # Verificar si ya existe un superusuario
        if Usuario.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Ya existe un superusuario'))
        else:
            # Crear domicilio por defecto si no existe
            domicilio, created = Domicilio.objects.get_or_create(
                calle="Calle Principal",
                numero_exterior="1",
                defaults={
                    'colonia': 'Centro',
                    'municipio': 'Ciudad',
                    'cp': '00000',
                    'ciudad': 'México'
                }
            )
            
            # Crear superusuario
            superuser = Usuario.objects.create_superuser(
                email='admin@admin.com',
                password='admin123',
                nombre='Admin',
                apellidos='Sistema',
                edad=30,
                universidad='N/A',
                carrera='N/A',
                ID_domicilio=domicilio,
                sensor_id=0  # Admin tiene sensor_id = 0
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Superusuario creado: {superuser.email}'))
            self.stdout.write(self.style.SUCCESS(f'   Password: admin123'))
            self.stdout.write(self.style.SUCCESS(f'   Sensor ID: 0'))

        # Crear usuario de prueba con huella si no existe
        if Usuario.objects.filter(sensor_id=5).exists():
            self.stdout.write(self.style.WARNING('Ya existe usuario con sensor_id=5'))
        else:
            # Obtener o crear domicilio
            domicilio, created = Domicilio.objects.get_or_create(
                calle="Calle Prueba",
                numero_exterior="123",
                defaults={
                    'colonia': 'Colonia',
                    'municipio': 'Municipio',
                    'cp': '12345',
                    'ciudad': 'Ciudad'
                }
            )
            
            # Crear usuario de prueba
            usuario = Usuario.objects.create_user(
                email='operador@prueba.com',
                password='prueba123',
                nombre='Operador',
                apellidos='De Prueba',
                edad=25,
                universidad='Universidad',
                carrera='Ingeniería',
                rol=2,  # Operador
                sensor_id=5,  # ID que usarás en el ESP32
                ID_domicilio=domicilio
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Usuario de prueba creado: {usuario.email}'))
            self.stdout.write(self.style.SUCCESS(f'   Password: prueba123'))
            self.stdout.write(self.style.SUCCESS(f'   Rol: Operador'))
            self.stdout.write(self.style.SUCCESS(f'   Sensor ID: 5'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Datos iniciales creados exitosamente'))
        self.stdout.write(self.style.SUCCESS('Puedes acceder al admin en: /admin/'))
        self.stdout.write(self.style.SUCCESS('Email: admin@admin.com | Password: admin123'))