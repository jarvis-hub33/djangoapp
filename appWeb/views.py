import openpyxl
from django.shortcuts import get_object_or_404, render, redirect
from appWeb.models import Paciente,Diagnostico
from appWeb.forms import PacienteForm
from django.contrib.auth.decorators import permission_required
from .models import HoraTomada,Paciente, Diagnostico,DiagnosticoUrg
from .forms import HoraTomadaForm,DiagnosticoForm,DiagnosticoUrgForm
from appWeb import models
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.views import View
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
import pandas as pd
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Medico
from .forms import MedicoForm









def medicos(request):
    medicos = Medico.objects.all()
    return render(request, 'appWeb/medicos.html', {'medicos': medicos})



def todas_medicos(request):
    medicos = Medicos.objects.all().order_by('nombre')
    data = {
        'medicos': medicos,
    }
    return render(request, 'appweb/medicos.html', data)

def agregar_medico(request):
    if request.method == "POST":
        form = MedicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('medicos')  # Redirige a la lista de médicos después de guardar
    else:
        form = MedicoForm()
    return render(request, 'appWeb/medicoadd.html', {'form': form})


def mostrar_medicos(request):
    medicos = medicos.objects.all()
    return render(request, "appWeb/medicos.html", {"medicos": medicos})  

def buscar_medicos(request):
    query = request.GET.get('q', '')
    medicos_list = Medico.objects.filter(nombre__icontains=query)
    return render(request, 'appWeb/medicos.html', {'medicos': medicos_list, 'query': query})



def cargar_editar_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    if request.method == 'POST':
        form = MedicoForm(request.POST, request.FILES, instance=medico)
        if form.is_valid():
            return redirect("medicos")
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'appWeb/medicoedit.html', {'form': form, 'medico': medico})





def editar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == "POST":
        form = MedicoForm(request.POST, request.FILES, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medicos')
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'appWeb/medicoadd.html', {'form': form, 'medico': medico})


def eliminar_medico(request, id):
    medico = get_object_or_404(Medico, id=id)
    if request.method == "POST":
        medico.delete()
        return redirect('medicos')
    return render(request, 'appWeb/medicodel.html', {'medico': medico})
   

@csrf_exempt
def analizar_excel(request):
    if request.method == 'POST' and request.FILES.get('file'):
        excel_file = request.FILES['file']
        try:
            # Leer el archivo Excel
            df = pd.read_excel(excel_file)

            # Verificar que las columnas necesarias existan
            required_columns = ['Enfermedad', 'Tipo de Atención', 'Especialidad']
            if not all(col in df.columns for col in required_columns):
                return JsonResponse({'error': 'El archivo no contiene las columnas requeridas: Enfermedad, Tipo de Atención, Especialidad'}, status=400)

            # Filtrar las columnas necesarias
            df = df[required_columns]

            detalles = []
            for _, row in df.iterrows():
                tipo_atencion = row['Tipo de Atención'].lower()
                enfermedad = row['Enfermedad']
                especialidad = row['Especialidad']

                # Generar respuestas "inteligentes" basadas en el tipo de atención
                if tipo_atencion == 'leve':
                    prediccion = {
                        'meses': 1,
                        'texto': f"El paciente con {enfermedad} bajo {especialidad} tiene una alta probabilidad de recuperación completa en 1 mes si sigue un tratamiento básico.",
                        'acciones': "Seguir una dieta saludable, evitar estrés excesivo y mantenerse hidratado."
                    }
                    consecuencias = "Si no sigue las recomendaciones, podría progresar a un estado moderado."
                elif tipo_atencion == 'moderada':
                    prediccion = {
                        'meses': 3,
                        'texto': f"El paciente con {enfermedad} bajo {especialidad} requiere atención médica regular. Podría recuperarse en 3 meses si sigue estrictamente las indicaciones médicas.",
                        'acciones': "Asistir a todas las consultas, seguir las recomendaciones médicas y reportar cualquier anomalía."
                    }
                    consecuencias = "Podría avanzar a un estado grave, reduciendo significativamente su calidad de vida."
                elif tipo_atencion == 'grave':
                    prediccion = {
                        'meses': 6,
                        'texto': f"El paciente con {enfermedad} bajo {especialidad} necesita tratamiento intensivo. La recuperación completa podría tomar 6 meses o más.",
                        'acciones': "Hospitalización inmediata, seguimiento constante y tratamiento especializado."
                    }
                    consecuencias = "Sin tratamiento adecuado, existe un alto riesgo de complicaciones críticas o irreversibles."
                else:
                    prediccion = {
                        'meses': 'Desconocido',
                        'texto': f"No hay suficientes datos para realizar una predicción sobre la enfermedad {enfermedad} en {especialidad}.",
                        'acciones': "Consultar con un especialista."
                    }
                    consecuencias = "Sin una evaluación adecuada, el estado del paciente podría deteriorarse."

                detalles.append({
                    'Enfermedad': enfermedad,
                    'Especialidad': especialidad,
                    'Tipo de Atención': row['Tipo de Atención'],
                    'Predicción': prediccion['texto'],
                    'Meses': prediccion['meses'],
                    'Recomendaciones': prediccion['acciones'],
                    'Consecuencias': consecuencias,
                })

            return JsonResponse({
                'mensaje': 'Análisis realizado con éxito',
                'detalles': detalles,
            })

        except Exception as e:
            return JsonResponse({'error': f'Error al procesar el archivo: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido o archivo no cargado'}, status=405)

















class RegisterView(View):
    form_class = RegisterForm  # El formulario de registro
    template_name = 'appweb/registro/registro.html'

    def get(self, request, *args, **kwargs):
        # Renderiza el formulario de registro
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Procesa el registro del usuario
        form = self.form_class(request.POST)  # Pasa solo los datos POST
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = False
            user.is_staff = False
            if not user.role:
                user.role = 'patient'  # Asigna el rol predeterminado
            user.save()  # Guarda el usuario en la base de datos

            messages.success(request, f"Cuenta creada exitosamente para {user.username}")
            return redirect('login')  # Redirige al inicio de sesión tras el registro exitoso
        else:
            messages.error(request, "Error al crear la cuenta. Revisa los datos ingresados.")
        
        # Si hay errores, vuelve a renderizar el formulario con mensajes de error
        return render(request, self.template_name, {'form': form})

         


def redirigir_por_rol(request):
    user = request.user
    print(f"Usuario autenticado: {user.username}, Rol: {user.role}")  # Debug para verificar

    if user.role == 'admin':
        print("Redirigiendo al dashboard de admin")
        return redirect('dashboard_admin')
    elif user.role == 'doctor':
        print("Redirigiendo al dashboard de doctor")
        return redirect('dashboard_doctor')
    elif user.role == 'patient':
        print("Redirigiendo al dashboard de paciente")
        return redirect('dashboard_paciente')
    else:
        print("Rol desconocido. Redirigiendo a la página de inicio.")
        return redirect('inicio')



def LoginView(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Autentica al usuario

            # Redirige según el rol del usuario
            return redirigir_por_rol(request)
    else:
        form = AuthenticationForm()

    return render(request, 'inicio.html', {'form': form})









def salir(request):
    try:
        logout(request)
        messages.success(request, '¡Has cerrado sesión correctamente!')
    except Exception as e:
        messages.error(request, f'Hubo un problema al cerrar sesión: {e}')
    return redirect('index')

def login(request):
    data = {
        'login':datos.login
    }
    return render(request,'registro/login.html',data)

def inicio(request):
    return render(request, "appWeb/inicio.html")

@permission_required("appWeb.add_paciente")
def crear_paciente(request):
    form = PacienteForm()
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pacientes')  # Cambia esto por la URL de tu lista de pacientes
    return render(request, 'appWeb/paciente.html', {'form': form})


@permission_required("appWeb.view_paciente")
def mostrar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, "appWeb/pacientes.html", {"pacientes": pacientes})  # Cambié a "pacientes.html"

@permission_required("appWeb.change_paciente")
def editar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == "POST":
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('pacientes')  # Redirige a la lista de pacientes
    else:
        form = PacienteForm(instance=paciente)
    return render(request, "appWeb/paciente.html", {'form': form, 'paciente': paciente})  # Cambié a "paciente.html"

def cargar_editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect("pacientes")  # Redirige a la vista donde se muestran los pacientes
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'appweb/pacienteEditar.html', {'form': form, 'paciente': paciente})

def todas_pacientes(request):
    categorias = Categoria.objects.all().order_by('nombre')
    data = {
        'pacientes': pacientes,
    }
    return render(request, 'appweb/pacientes.html', data)


def buscar_pacientes(request):
    query = request.GET.get('q', '')  # Obtiene el término de búsqueda
    pacientes = Paciente.objects.all()  # Por defecto, mostramos todos los pacientes

    if query:
        pacientes = pacientes.filter(nombre__icontains=query)  # Filtra solo por nombre

    # Si la solicitud es AJAX, solo devolvemos el fragmento de la tabla
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'appweb/pacientes_results.html', {'pacientes': pacientes})

    # Si no es AJAX, renderizamos la página completa
    return render(request, 'appweb/pacientes.html', {'pacientes': pacientes})

@permission_required("appWeb.delete_paciente")
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == "POST":
        paciente.delete()
        return redirect("pacientes")  # Redirige a la lista de pacientes
    return render(request, "appWeb/pacienteDel.html", {"paciente": paciente})  # Cambié a "pacienteDel.html"



def diagnosticos_dashboard(request):
    pacientes = Paciente.objects.all()  # Lista de pacientes
    selected_paciente = None
    diagnosticos = []
    labels = []
    values = []
    comentario = None
    datos_paciente = None

    # Verificar si se seleccionó un paciente
    if request.GET.get('paciente_id'):
        paciente_id = request.GET.get('paciente_id')
        selected_paciente = get_object_or_404(Paciente, id=paciente_id)
        diagnosticos = Diagnostico.objects.filter(paciente=selected_paciente)

        # Calcular cantidad de cada tipo de diagnóstico
        diagnostico_counts = diagnosticos.values('tipo').annotate(cantidad=models.Count('tipo')).order_by('tipo')

        # Preparar los datos para el gráfico
        labels = [item['tipo'] for item in diagnostico_counts]
        values = [item['cantidad'] for item in diagnostico_counts]

        # Datos del paciente
        datos_paciente = {
            'nombre': f"{selected_paciente.nombre} {selected_paciente.paterno} {selected_paciente.materno}",
            'edad': calcular_edad(selected_paciente.fechaNac),
            'enfermedades': [diag.tipo for diag in diagnosticos],
        }

        # Generar comentario basado en diagnósticos
        enfermedades = [diag.tipo.lower() for diag in diagnosticos]
        if 'cáncer' in enfermedades:
            comentario = "Se requiere atención inmediata y tratamiento crítico."
        elif 'gripe' in enfermedades:
            comentario = "Se sugiere reposo y mantenerse hidratado."
        elif 'resfriado' in enfermedades:
            comentario = "Se recomienda descanso y evitar actividades físicas."
        else:
            comentario = "Consulta a un médico para más información."

    # Manejar el formulario para agregar diagnóstico
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            if selected_paciente is None:
                messages.error(request, "Debe seleccionar un paciente antes de agregar un diagnóstico.")
                return redirect('diagnosticos_dashboard')

            diagnostico = form.save(commit=False)
            diagnostico.paciente = selected_paciente  # Asignar paciente automáticamente
            diagnostico.save()
            messages.success(request, "Diagnóstico agregado exitosamente.")
            return redirect(f'/diagnosticos_dashboard/?paciente_id={selected_paciente.id}')
        else:
            messages.error(request, "Error al guardar el diagnóstico. Por favor, revise los datos.")
    else:
        form = DiagnosticoForm()

    context = {
        'pacientes': pacientes,
        'selected_paciente': selected_paciente,
        'form': form,
        'labels': labels,
        'values': values,
        'datos_paciente': datos_paciente,
        'comentario': comentario,
    }

    return render(request, 'appWeb/diagnosticos_dashboard.html', context)



def calcular_edad(fecha_nacimiento):
    from datetime import date
    if fecha_nacimiento:
        today = date.today()
        return (
            today.year - fecha_nacimiento.year - 
            ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        )
    return "Fecha no registrada"


def pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'appWeb/pacientes.html', {'pacientes': pacientes})


    
def informe_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    # Asumiendo que 'nivel_riesgo' es un campo de tu modelo Diagnóstico relacionado al paciente
    diagnosticos = paciente.diagnosticos.all()  # O cualquier otro campo que contenga los diagnósticos
    return render(request, 'appWeb/informe_paciente.html', {
        'paciente': paciente,
        'diagnosticos': diagnosticos
    })# Actualicé el nombre del template

def horas_disponibles(request):
    return render(request, "appWeb/horas_disponibles.html")  # Actualicé el nombre del template

def agendar_hora(request):
    return render(request, "appWeb/agendar_hora.html")  # Actualicé el nombre del template


def buscar_horas_tomadas(request):
    query = request.GET.get('q', '')  # Obtiene el término de búsqueda
    horas = HoraTomada.objects.all()  # Por defecto, mostramos todas las horas tomadas

    if query:
        # Filtra por nombre, médico o especialidad que coincidan con el término de búsqueda
        horas = horas.filter(
            nombre__icontains=query
        ) | horas.filter(
            medico__icontains=query
        ) | horas.filter(
            especialidad__icontains=query
        )

    # Si la solicitud es AJAX, solo devolvemos el fragmento de la tabla
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'appweb/horas_tomadas_results.html', {'horas': horas})

    # Si no es AJAX, renderizamos la página completa
    return render(request, 'appweb/listar_horas_tomadas.html', {'horas': horas})



def listar_horas_tomadas(request):
    horas = HoraTomada.objects.all()
    return render(request, "appWeb/listar_horas_tomadas.html", {"horas": horas})



def agregar_hora_tomada(request):
    if request.method == "POST":
        form = HoraTomadaForm(request.POST)
        if form.is_valid():
            hora_tomada = form.save()

            # Enviar correo de confirmación
            if hora_tomada.correo:
                send_mail(
                    'Confirmación de Hora Agendada',
                    f'Estimado/a {hora_tomada.nombre},\n\nSu hora ha sido agendada con éxito.\n\nDetalles:\nMédico: {hora_tomada.medico}\nEspecialidad: {hora_tomada.especialidad}\nLugar: {hora_tomada.lugar_de_atencion}\n\nGracias por confiar en nuestro servicio.',
                    'tuemail@example.com',  # Cambia esto por tu email
                    [hora_tomada.correo],
                    fail_silently=False,
                )
                messages.success(request, 'La hora fue agendada y el correo fue enviado.')
            else:
                messages.warning(request, 'La hora fue agendada, pero no se proporcionó un correo para enviar la confirmación.')

            return redirect("listar_horas_tomadas")
    else:
        form = HoraTomadaForm()

    # Obtener todos los pacientes para usarlos en el menú desplegable
    pacientes = Paciente.objects.all()

    return render(request, "appWeb/agregar_hora_tomada.html", {
        "form": form,
        "pacientes": pacientes  # Agregamos los pacientes al contexto
    })



@permission_required("appWeb.change_hora tomada", raise_exception=True)
def editar_hora_tomada(request, id):
    hora = get_object_or_404(HoraTomada, id=id)
    if request.method == "POST":
        form = HoraTomadaForm(request.POST, instance=hora)
        if form.is_valid():
            form.save()
            return redirect("listar_horas_tomadas")
    else:
        form = HoraTomadaForm(instance=hora)
    return render(request, "appWeb/editar_hora_tomada.html", {"form": form, "hora": hora})


@permission_required("appWeb.delete_hora tomada", raise_exception=True)
def eliminar_hora_tomada(request, id):
    hora = get_object_or_404(HoraTomada, id=id)
    if request.method == "POST":
        hora.delete()
        return redirect("listar_horas_tomadas")
    return render(request, "appWeb/eliminar_hora_tomada.html", {"hora": hora})


def informe_paciente(request, paciente_id):  # Cambia 'id' por 'paciente_id'
    # Obtener el paciente y sus diagnósticos
    paciente = get_object_or_404(Paciente, id=paciente_id)
    diagnosticos = Diagnostico.objects.filter(paciente=paciente)

    # Crear un contexto con los detalles del paciente y sus diagnósticos
    contexto = {
        "paciente": paciente,
        "nombre_completo": f"{paciente.nombre} {paciente.paterno} {paciente.materno}",
        "diagnosticos": diagnosticos,
        "edad": calcular_edad(paciente.fechaNac),
    }

    return render(request, "appWeb/informe_paciente.html", contexto)

def informe_excel(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    # Asegúrate de extraer los valores de los objetos relacionados
    tipo_atencion = paciente.tipoatencion.nombre  # Asumiendo que 'nombre' es un campo en el modelo 'Tipo_Atencion'
    
    # El resto de tu código para exportar a Excel sigue aquí.
    # ...
def informe_excel(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    # Crear un archivo Excel en memoria
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Informe Paciente"

    # Definir los encabezados
    headers = [
        'RUN', 'Nombre', 'Apellido Paterno', 'Apellido Materno', 'Sexo', 'Enfermedad', 
        'Fecha de Nacimiento', 'Tipo de Atención', 'Especialidad'
    ]
    ws.append(headers)

    # Extraer los datos del paciente
    data = [
        paciente.run,
        paciente.nombre,
        paciente.paterno,
        paciente.materno,
        paciente.sexo,
        paciente.enfermedad,
        paciente.fechaNac.strftime('%d/%m/%Y'),  # Formatear la fecha
        paciente.tipoatencion.nombre,  # Extraer nombre de Tipo_Atencion
        paciente.especialidad.nombre  # Extraer nombre de Especialidad
    ]

    # Escribir los datos en el archivo Excel
    ws.append(data)

    # Preparar la respuesta para descargar el archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=Informe_Paciente_{paciente_id}.xlsx'
    
    # Guardar el archivo Excel en la respuesta
    wb.save(response)
    return response


def informe_pdf(request, paciente_id):
    paciente = Paciente.objects.get(id=paciente_id)

    # Crear una respuesta Http con el contenido de tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Informe_Paciente_{paciente_id}.pdf'

    # Crear el canvas para el PDF
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Definir las posiciones y el tamaño de la fuente
    x_field = 50  # Posición para los campos (izquierda)
    x_value = 200  # Posición para los valores (derecha)
    y_offset = height - 50
    line_height = 20

    # Datos del paciente
    fields_and_values = [
        ("RUN", paciente.run),
        ("Nombre", paciente.nombre),
        ("Apellido Paterno", paciente.paterno),
        ("Apellido Materno", paciente.materno),
        ("Sexo", paciente.sexo),
        ("Enfermedad", paciente.enfermedad),
        ("Fecha de Nacimiento", paciente.fechaNac.strftime('%d/%m/%Y') if paciente.fechaNac else "N/A"),
        ("Tipo de Atención", paciente.tipoatencion.nombre),
        ("Especialidad", paciente.especialidad.nombre),
    ]

    # Título del informe
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_offset, "Informe del Paciente")
    y_offset -= 40  # Espacio debajo del título

    # Dibujar cada campo y valor en la tabla
    c.setFont("Helvetica", 12)
    for field, value in fields_and_values:
        c.drawString(x_field, y_offset, field)  # Campo
        c.drawString(x_value, y_offset, str(value))  # Valor
        y_offset -= line_height

    # Finalizar el PDF
    c.showPage()
    c.save()

    return response

    
def calcular_edad(fecha_nacimiento):
    from datetime import date
    if fecha_nacimiento:
        today = date.today()
        return (
            today.year - fecha_nacimiento.year - 
            ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        )
    return "Fecha de nacimiento no registrada"

def agregar_diagnostico_urgente(request):
    if request.method == 'POST':
        form = DiagnosticoUrgForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Diagnóstico urgente guardado exitosamente.")
            return redirect('diagnosticos_dashboard')  # Cambia según el flujo deseado
    else:
        form = DiagnosticoUrgForm()

    return render(request, 'appWeb/agregar_diagnostico_urgente.html', {'form': form})




@login_required
def dashboard_admin(request):
    horas = HoraTomada.objects.values('nombre', 'fecha_nacimiento')
    eventos = [
        {
            "title": hora['nombre'],
            "start": hora['fecha_nacimiento'].isoformat()  # Convertimos la fecha a formato ISO
        }
        for hora in horas if hora['fecha_nacimiento']  # Filtramos los registros con fecha válida
    ]
    return render(request, 'appWeb/dashboard_admin.html', {
        'eventos': json.dumps(eventos, cls=DjangoJSONEncoder)
    })

@login_required
def dashboard_doctor(request):
    horas = HoraTomada.objects.values('nombre', 'fecha_nacimiento')
    eventos = [
        {
            "title": hora['nombre'],
            "start": hora['fecha_nacimiento'].isoformat()  # Convertimos la fecha a formato ISO
        }
        for hora in horas if hora['fecha_nacimiento']  # Filtramos los registros con fecha válida
    ]
    return render(request, 'appWeb/dashboard_doctor.html', {
        'eventos': json.dumps(eventos, cls=DjangoJSONEncoder)
    })

@login_required
def dashboard_paciente(request):
    horas = HoraTomada.objects.values('nombre', 'fecha_nacimiento')
    eventos = [
        {
            "title": hora['nombre'],
            "start": hora['fecha_nacimiento'].isoformat()  # Convertimos la fecha a formato ISO
        }
        for hora in horas if hora['fecha_nacimiento']  # Filtramos los registros con fecha válida
    ]
    return render(request, 'appWeb/dashboard_paciente.html', {
        'eventos': json.dumps(eventos, cls=DjangoJSONEncoder)
    })



def diagnosticos_dashboard(request):
    pacientes = Paciente.objects.all()
    selected_paciente = None
    labels = []
    values = []

    if request.GET.get('paciente_id'):
        paciente_id = request.GET.get('paciente_id')
        selected_paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = DiagnosticoUrgForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda los datos en la tabla DiagnosticoUrg
            messages.success(request, "Diagnóstico agregado exitosamente.")
            return redirect('diagnosticos_dashboard')
        else:
            messages.error(request, "Error al guardar el diagnóstico.")
    else:
        form = DiagnosticoUrgForm()

    context = {
        'pacientes': pacientes,
        'selected_paciente': selected_paciente,
        'form': form,
        'labels': labels,
        'values': values,
    }

    return render(request, 'appWeb/diagnosticos_dashboard.html', context)