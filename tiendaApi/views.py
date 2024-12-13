from django.shortcuts import render
from appWeb.models import Paciente
from django.http import JsonResponse
# Create your views here.





def pacientesApi(request):
    # Recuperar todos los pacientes de la base de datos
    pacientes = Paciente.objects.all()

    # Convertir los datos en una lista de diccionarios con los campos requeridos
    data = {
        'pacientes': list(
            pacientes.values(
                'run', 'nombre', 'paterno', 'materno', 'sexo', 'enfermedad', 
                'fechaNac', 'tipoatencion__nombre', 'especialidad__nombre'
            )
        )
    }

    # Retornar los datos en formato JSON
    return JsonResponse(data)