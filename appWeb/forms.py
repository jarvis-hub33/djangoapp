from django import forms
from appWeb.choices import sexos
from appWeb.models import Tipo_Atencion, Especialidad, Paciente
from .models import Diagnostico, Cita, HoraTomada, CustomUser,DiagnosticoUrg
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Medico
# Opciones de selección adicionales
ENFERMEDADES = [
    ('diabetes', 'Diabetes'),
    ('hipertension', 'Hipertensión'),
    ('asma', 'Asma'),
    # Agrega más enfermedades aquí
]

ODONTOLOGIA_ESPECIALIDADES = [
    ('ortodoncia', 'Ortodoncia'),
    ('endodoncia', 'Endodoncia'),
    ('periodoncia', 'Periodoncia'),
    # Agrega más especialidades aquí
]

REMEDIOS = [
    ('paracetamol', 'Paracetamol'),
    ('ibuprofeno', 'Ibuprofeno'),
    ('amoxicilina', 'Amoxicilina'),
    # Agrega más remedios aquí
]

from django import forms
from .models import Paciente

from django import forms
from .models import Paciente




class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirm_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', ]  # Solo incluye los campos necesarios

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Cifra la contraseña
        if commit:
            user.save()
        return user


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')


        
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'run': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese RUN'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombre'}),
            'paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Apellido Paterno'}),
            'materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Apellido Materno'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'enfermedad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Enfermedad'}),
            'fechaNac': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipoatencion': forms.Select(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
        }


    def clean_fechaNac(self):
        fecha_nac = self.cleaned_data.get("fechaNac")
        fecha_minima = datetime.date(1900, 1, 1)
        if fecha_nac and fecha_nac < fecha_minima:
            raise forms.ValidationError("La fecha de nacimiento debe ser posterior a 1900.")
        return fecha_nac


class DiagnosticoForm(forms.ModelForm):
    tipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de diagnóstico'}))
    nivel_riesgo = forms.ChoiceField(choices=[
        ('bajo', 'Bajo'),
        ('medio', 'Medio'),
        ('alto', 'Alto'),
    ], widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Diagnostico
        fields = ['tipo', 'nivel_riesgo']


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['nombre', 'edad', 'rut', 'problema']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Paciente'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RUT'}),
            'problema': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa el problema', 'rows': 3}),
        }


class AgendarCitaForm(forms.ModelForm):
    enfermedades = forms.ChoiceField(choices=ENFERMEDADES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    odontologia_especialidad = forms.ChoiceField(choices=ODONTOLOGIA_ESPECIALIDADES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    remedios = forms.ChoiceField(choices=REMEDIOS, required=False, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Cita
        fields = ['nombre', 'edad', 'especialidad', 'problema']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Paciente'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Edad'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'problema': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa el problema', 'rows': 3}),
        }


class HoraTomadaForm(forms.ModelForm):
    class Meta:
        model = HoraTomada
        fields = [
            'nombre', 
            'paterno', 
            'materno', 
            'sexo', 
            'enfermedad', 
            'fecha_nacimiento', 
            'medico', 
            'especialidad', 
            'lugar_de_atencion', 
            'correo'
        ]
        
        widgets = {
            'nombre': forms.Select(attrs={'class': 'form-select'}),
            'paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Paterno'}),
            'materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido Materno'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'enfermedad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Enfermedad'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'medico': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Especialidad'}),
            'lugar_de_atencion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lugar de Atención'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password','role')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role')



class DiagnosticoUrgForm(forms.ModelForm):
    class Meta:
        model = DiagnosticoUrg
        fields = ['paciente', 'enfermedad', 'nivel_riesgo']
        labels = {
            'paciente': 'Nombre del Paciente',
            'enfermedad': 'Enfermedad',
            'nivel_riesgo': 'Nivel de Riesgo',
        }
        widgets = {
            'paciente': forms.TextInput(attrs={'class': 'form-control'}),
            'enfermedad': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_riesgo': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('bajo', 'Riesgo Bajo'),
                ('medio', 'Riesgo Medio'),
                ('alto', 'Riesgo Alto'),
            ]),
        }




class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['run', 'nombre', 'sexo', 'especialidad', 'tipo_atencion', 'foto']
        widgets = {
            'run': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese RUN'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombre'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'tipo_atencion': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }