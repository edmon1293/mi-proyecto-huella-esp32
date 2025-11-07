from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Domicilio, Usuario, Contacto
from .models import Documento


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'archivo')
    search_fields = ('nombre',)

class UsuarioAdmin(BaseUserAdmin):
    model = Usuario
    list_display = ('email', 'nombre', 'apellidos', 'edad', 'universidad', 'carrera', 'rol', 'is_active', 'INE', 'CURP', 'COMPROBANTE_DOMICILIO', 'ACTA_NACIMIENTO', 'CONSTANCIA_DERECHOS')
    list_filter = ('is_active', 'rol')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre', 'apellidos', 'edad', 'universidad', 'carrera', 'ID_domicilio', 'INE', 'CURP', 'COMPROBANTE_DOMICILIO', 'ACTA_NACIMIENTO', 'CONSTANCIA_DERECHOS')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # Eliminar 'Important dates' si no tienes estos campos en tu modelo
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nombre', 'apellidos', 'edad', 'universidad', 'carrera', 'ID_domicilio', 'rol', 'INE', 'CURP', 'COMPROBANTE_DOMICILIO', 'ACTA_NACIMIENTO', 'CONSTANCIA_DERECHOS'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)



# Registra los modelos con las configuraciones adecuadas
admin.site.register(Domicilio)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Contacto)
