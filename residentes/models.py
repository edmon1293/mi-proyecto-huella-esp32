from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('rol', 3)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        domicilio_predeterminado = Domicilio.objects.first()
        extra_fields.setdefault('ID_domicilio', domicilio_predeterminado)

        return self.create_user(email, password, **extra_fields)
    

class Domicilio(models.Model):
    ID_domicilio = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=100)
    numero_exterior = models.CharField(max_length=10)
    colonia = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    cp = models.CharField(max_length=10)
    ciudad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.calle} {self.numero_exterior}, {self.colonia}, {self.municipio}, {self.cp}, {self.ciudad}"

class Usuario(AbstractBaseUser, PermissionsMixin):
    ID_usuario = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    edad = models.IntegerField(null=True, blank=True)
    universidad = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    ID_domicilio = models.ForeignKey(Domicilio, on_delete=models.CASCADE, null=True, blank=True)
    rol = models.IntegerField(default=1)  # 1: usuario, 2: operador, 3: admin
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    sensor_id = models.IntegerField(unique=True, null=True, blank=True)
    INE = models.FileField(upload_to='pdfs/', null=True, blank=True)
    CURP = models.FileField(upload_to='pdfs/', null=True, blank=True)
    COMPROBANTE_DOMICILIO = models.FileField(upload_to='pdfs/', null=True, blank=True)
    ACTA_NACIMIENTO = models.FileField(upload_to='pdfs/', null=True, blank=True)
    CONSTANCIA_DERECHOS = models.FileField(upload_to='pdfs/', null=True, blank=True)


    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Contacto(models.Model):
    ID_contacto = models.AutoField(primary_key=True)
    ID_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contacto = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.contacto} ({self.tipo})"
    
class Documento(models.Model):
    nombre = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='documentos/')  # Campo para subir archivos

    def __str__(self):
        return self.nombre

