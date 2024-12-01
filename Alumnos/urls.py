from django.urls import path
from .views import alumno_login, dashboard_alumno,datosPersonales_alumno, actualizarDatos_alumno, changePassword_alumno, datosInvestigacion_alumno, buscar_estudiante, guardarInvestigacion, tramites_alumno, generar_pdf, registrar_carta_acceso, evaluacion_alumno, actualizar_dictamen, actualizar_asignacion, logout_view, reestablecerPassword_alumno, resetear_contrasena

#Create your urls here.
urlpatterns = [
    path('login/', alumno_login, name='alumno_login'),
    path('dashboard/', dashboard_alumno, name='dashboard_alumno'),
    path('logout/', logout_view, name='logout'),
    path('datospersonales/', datosPersonales_alumno, name='datosPersonales_alumno'),
    path('datospersonales/actualizar-datos/', actualizarDatos_alumno, name='actualizarDatos_alumno'),
    path('datospersonales/changepassword/', changePassword_alumno, name='changePassword_alumno'),
    path('datosinvestigacion/', datosInvestigacion_alumno, name='datosInvestigacion_alumno'),
    path('datosinvestigacion/buscarestudiante/', buscar_estudiante, name='buscar_estudiante'),
    path('datosinvestigacion/guardarinvestigacion/', guardarInvestigacion, name='guardarInvestigacion'),
    path('tramites/', tramites_alumno, name='tramites_alumno'),
    path('tramites/<int:proyecto_id>/<int:semestre_id>/pdf/', generar_pdf, name='generar_pdf'),
    path('tramites/registrar-carta/', registrar_carta_acceso, name='registrar_carta_acceso'),
    path('evaluacion/', evaluacion_alumno, name='evaluacion_alumno'),
    path('evaluacion/actualizar-dictamen', actualizar_dictamen, name='actualizar_dictamen'),
    path('evaluacion/sendlink', actualizar_asignacion, name='actualizar_asignacion'),
    path('reestablecer-password/', reestablecerPassword_alumno, name='reestablecerPassword_alumno'),
    path('resetear-password/', resetear_contrasena, name='resetear_contrasena')
]
