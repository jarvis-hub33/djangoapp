from django.contrib import admin
from django.urls import path, include
from appWeb import views as vista, views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tiendaApi import views as vistasApi
from appWeb.views import RegisterView  


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vista.inicio, name="inicio"),
    path('paciente/', vista.crear_paciente, name="paciente"),
    path('pacientes/', vista.mostrar_pacientes, name="pacientes"),
    path('buscar_pacientes/', vista.buscar_pacientes, name='buscar_pacientes'),
    path('pacienteEditar/<int:paciente_id>/', vista.cargar_editar_paciente, name='pacienteEditar'),
    path('pacienteEditado/<int:id>/', vista.editar_paciente, name='pacienteEditado'),
    path('pacienteDel/<int:id>/', vista.eliminar_paciente, name='pacienteDel'),
    path('medicos/', vista.medicos, name='medicos'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('registro/', RegisterView.as_view(), name='registro'),
    path('dashboard/', vista.diagnosticos_dashboard, name='diagnosticos_dashboard'),
    path('informe/<int:paciente_id>/', vista.informe_paciente, name='informe_paciente'),
    path('informe/excel/<int:paciente_id>/', vista.informe_excel, name='informe_excel'),
    path('informe/pdf/<int:paciente_id>/', vista.informe_pdf, name='informe_pdf'),
    path('horas/', vista.horas_disponibles, name='horas_disponibles'),
    path('agendar/<int:hora_id>/', vista.agendar_hora, name='agendar_hora'),
    path('horas_tomadas/', vista.listar_horas_tomadas, name='listar_horas_tomadas'),
    path('agregar_hora/', views.agregar_hora_tomada, name='agregar_hora_tomada'),
    path('horas_tomadas/editar/<int:id>/', vista.editar_hora_tomada, name='editar_hora_tomada'),
    path('horas_tomadas/eliminar/<int:id>/', vista.eliminar_hora_tomada, name='eliminar_hora_tomada'),
    path('pacientesApi/',vistasApi.pacientesApi,name='pacientesApi'),
    path('horas_tomadas/buscar/', vista.buscar_horas_tomadas, name='buscar_horas_tomadas'),

    path('analizar_excel/', vista.analizar_excel, name='analizar_excel'),
 
    path('medicos/agregar/', vista.agregar_medico, name='medico'),  # Asegúrate de que 'medico' esté definido aquí
    path('medicos/', vista.medicos, name='medicos'),
    path('medicos/buscar/', vista.buscar_medicos, name='buscar_medicos'),
    path('medicoseditar/<int:medico_id>/', vista.cargar_editar_medico, name='medicoeditar'),
    path('medicoseditado/<int:id>/', vista.editar_medico, name='medicoeditado'),
    path('medicosdel/<int:id>/', vista.eliminar_medico, name='eliminarmedico'),




    # Rutas para los dashboards por roles
    path('admin-panel/dashboard/', views.dashboard_admin, name='dashboard_admin'),
    path('doctor/dashboard/', views.dashboard_doctor, name='dashboard_doctor'),
    path('paciente/dashboard/', views.dashboard_paciente, name='dashboard_paciente'),
    path('redirigir/', views.redirigir_por_rol, name='redirigir_por_rol'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)