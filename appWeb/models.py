import os
from django.db import models
from django.utils import timezone
from appWeb.choices import sexos
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser



# Especialidades
ESPECIALIDADES = [
    ('odontologia', 'Odontología'),
    ('medicina_general', 'Medicina General'),
    ('retiro_insumos', 'Retiro de Insumos'),
]




class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('doctor', 'Doctor'),
        ('patient', 'Paciente'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"










class Tipo_Atencion(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre del Tipo de Atención')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):  # Cambia _str_ a __str__
        return f"{self.nombre}"

    class Meta:
        db_table = 'tipoatencion'
        verbose_name = 'Tipo de Atención'
        verbose_name_plural = 'Tipos de Atenciones'


class Especialidad(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name='Nombre de la Especialidad')
    descripcion = models.TextField(null=True, blank=True, verbose_name='Descripción')  # Nuevo campo
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        db_table = 'especialidad'
        verbose_name = 'Especialidad'
        verbose_name_plural = 'Especialidades'






class Medico(models.Model):
    run = models.CharField(max_length=12, verbose_name="RUN")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], verbose_name="Sexo")
    especialidad = models.ForeignKey(Especialidad, null=False, on_delete=models.CASCADE)
    tipo_atencion = models.ForeignKey(Tipo_Atencion, null=False, on_delete=models.RESTRICT, verbose_name="Tipo de Atención")
    foto = models.ImageField(upload_to='medicos/', verbose_name="Fotografía", null=True, blank=True)

    def __str__(self):
        return self.nombre






class Paciente(models.Model):
    run = models.CharField(max_length=10, verbose_name="RUN")
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    paterno = models.CharField(max_length=50, verbose_name="Apellido Paterno")
    materno = models.CharField(max_length=50, verbose_name="Apellido Materno")
    sexo = models.CharField(max_length=1, choices=sexos, default='o')
    enfermedad = models.CharField(max_length=200, verbose_name="Enfermedad")    
    fechaNac = models.DateField(blank=True, null=True, verbose_name="Fecha de nacimiento")
    tipoatencion = models.ForeignKey(Tipo_Atencion, null=False, on_delete=models.RESTRICT, verbose_name="Tipo de Atencion")
    especialidad = models.ForeignKey(Especialidad, null=False, on_delete=models.CASCADE)
    creado = models.DateTimeField(default=timezone.now, editable=False)
    diagnosticos = models.ManyToManyField('Diagnostico', related_name="pacientes", blank=True)


    def generar_nombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = 'pacientes'
        fecha = timezone.now().strftime('%d%m%Y_%H%M%S')
        nombre = f"{fecha}.{extension}"
        return os.path.join(ruta, nombre)

    foto = models.ImageField(upload_to=generar_nombre, null=True, blank=True, default='pacientes/paciente.png')
    def __str__(self):
        return f"{self.nombre}"






    @property
    def edad(self):
        """Calcula la edad del paciente en función de su fecha de nacimiento."""
        if self.fechaNac:
            from datetime import date
            today = date.today()
            return today.year - self.fechaNac.year - (
                (today.month, today.day) < (self.fechaNac.month, self.fechaNac.day)
            )
        return None  # Si no tiene fecha de nacimiento registrada

    def _str_(self):
        return f"{self.nombre} {self.paterno} {self.materno}"

    class Meta:
        db_table = "paciente"
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ["nombre", "paterno", "materno", "tipoatencion", "especialidad"]


class Diagnostico(models.Model):
    paciente = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)  # Tipo de diagnóstico
    nivel_riesgo = models.CharField(max_length=50)  # Nivel de riesgo
    creado = models.DateTimeField(auto_now_add=True)  # Solo se establece al crear el registro

    def _str_(self):
        return f"{self.tipo} - {self.nivel_riesgo}"

    @staticmethod
    def contar_diagnosticos_por_paciente(paciente, tipo):
        """Cuenta cuántas veces un paciente ha recibido un diagnóstico específico."""
        return Diagnostico.objects.filter(paciente=paciente, tipo=tipo).count()



class HoraDisponible(models.Model):
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDADES)
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.get_especialidad_display()} - {self.hora} ({'Disponible' if self.disponible else 'Ocupada'})"


class Cita(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    rut = models.CharField(max_length=12, blank=True, null=True)
    problema = models.TextField(blank=True, null=True)
    especialidad = models.CharField(max_length=50, choices=ESPECIALIDADES)
    hora = models.ForeignKey(HoraDisponible, on_delete=models.CASCADE)
    fecha = models.DateField(default=now)

    def _str_(self):
        return f"Cita: {self.nombre or 'Anónimo'} - {self.get_especialidad_display()} - {self.hora.hora}"
    

class HoraTomada(models.Model):

    nombre = models.ForeignKey(Paciente, null=False, on_delete=models.CASCADE)
    paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno", null=True, blank=True)
    materno = models.CharField(max_length=100, verbose_name="Apellido Materno", null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=sexos, verbose_name="Sexo", null=True, blank=True)
    enfermedad = models.CharField(max_length=200, verbose_name="Enfermedad", null=True, blank=True)
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    medico = models.ForeignKey(Medico, null=False, on_delete=models.RESTRICT, verbose_name="Eliga Medico")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad", null=True, blank=True)
    lugar_de_atencion = models.CharField(max_length=100, verbose_name="Lugar de Atención", null=True, blank=True)
    correo = models.EmailField(max_length=254, verbose_name="Correo Electrónico", null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.paterno} - {self.medico}"

    class Meta:
        db_table = "hora_tomada"
        verbose_name = "Hora Tomada"
        verbose_name_plural = "Horas Tomadas"



class DiagnosticoUrg(models.Model):
    paciente = models.CharField(max_length=255, verbose_name="Nombre del Paciente")
    enfermedad = models.CharField(max_length=255, verbose_name="Enfermedad")
    nivel_riesgo = models.CharField(max_length=50, verbose_name="Nivel de Riesgo")
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def _str_(self):
        return f"{self.paciente} - {self.enfermedad} ({self.nivel_riesgo})"

    class Meta:
        db_table = "diagnosticosurg"
        verbose_name = "Diagnóstico Urgente"
        verbose_name_plural = "Diagnósticos Urgentes"