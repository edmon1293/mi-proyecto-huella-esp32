from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Domicilio, Contacto
from .models import Documento

class SuperUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'password1', 'password2')

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)
    # Campos adicionales para Domicilio y Contacto
    calle = forms.CharField(max_length=100)
    numero_exterior = forms.CharField(max_length=10)
    colonia = forms.CharField(max_length=50)
    municipio = forms.CharField(max_length=50)
    cp = forms.CharField(max_length=10)
    ciudad = forms.CharField(max_length=50)
    contacto = forms.CharField(max_length=100)
    tipo = forms.CharField(max_length=50)
    INE = forms.FileField(required=False)
    CURP = forms.FileField(required=False)
    COMPROBANTE_DOMICILIO = forms.FileField(required=False)
    ACTA_NACIMIENTO = forms.FileField(required=False)
    CONSTANCIA_DERECHOS = forms.FileField(required=False)

    class Meta:
        model = Usuario
        fields = [
            'email', 'password', 'confirmar_password', 'nombre', 'apellidos',
            'edad', 'universidad', 'carrera', 'INE', 'CURP', 'COMPROBANTE_DOMICILIO', 'ACTA_NACIMIENTO', 'CONSTANCIA_DERECHOS'
        ]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")
        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data
    
class BusquedaForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=100)

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre', 'archivo'] 
