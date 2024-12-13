from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tipo_Atencion, Especialidad, Paciente, Diagnostico
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Medico
# Register your models here.

class Tipo_AtencionAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre"]

class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ["codigo", "nombre"]

class PacienteAdmin(admin.ModelAdmin):
    list_display = ["run", "nombre", "paterno", "tipoatencion", "especialidad", "mostrar_diagnosticos"]

    @admin.display(description="Diagnósticos")
    def mostrar_diagnosticos(self, obj):
        """Muestra una lista de diagnósticos asociados a un paciente."""
        return ", ".join([diag.tipo for diag in obj.diagnosticos.all()])

class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ["id", "tipo", "nivel_riesgo", "paciente", "creado"]

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'role')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ['username', 'email']
    ordering = ['username']

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('run', 'nombre', 'sexo', 'especialidad', 'tipo_atencion')  # Campos visibles en la lista
    search_fields = ('run', 'nombre')  # Campos para la barra de búsqueda
    list_filter = ('sexo', 'especialidad')  # Filtros disponibles en la interfaz

# Registra el modelo con su configuración de administración
admin.site.register(Medico, MedicoAdmin)
# Registra las clases de admin
admin.site.register(Tipo_Atencion, Tipo_AtencionAdmin)
admin.site.register(Especialidad, EspecialidadAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Diagnostico, DiagnosticoAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

