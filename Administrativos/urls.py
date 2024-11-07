from django.urls import path
from .views import administrativo_login, dashboard_administrativo, datosPersonales_admin, actualizarDatos_admin, changePassword_admin, tramites_admin, actualizar_observacion, enviar_respuesta, asignacionJurado_admin, actualizar_jurados, eliminar_jurados, seguimiento_admin, logout_view, reestablecerPassword_admin, resetear_contrasena

#Create your urls here.
urlpatterns = [
    path('login/', administrativo_login, name='administrativo_login'),
    path('dashboard/', dashboard_administrativo, name='dashboard_administrativo'),
    path('logout/', logout_view, name='logout'),
    path('datospersonales/', datosPersonales_admin, name='datosPersonales_admin'),
    path('datospersonales/actualizar-datos/', actualizarDatos_admin, name='actualizarDatos_admin'),
    path('datospersonales/changepassword/', changePassword_admin, name='changePassword_admin'),
    path('tramites/', tramites_admin, name='tramites_admin'),
    path('tramites/actualizar_observacion/', actualizar_observacion, name='actualizar_observacion'),
    path('tramites/enviar-respuesta/', enviar_respuesta, name='enviar_respuesta'),
    path('asignacion-jurado/', asignacionJurado_admin, name='asignacionJurado_admin'),
    path('asignacion-jurado/actualizar-jurado/', actualizar_jurados, name='actualizar_jurados'),
    path('asignacion-jurado/eliminar-jurado/', eliminar_jurados, name='eliminar_jurados'),
    path('seguimiento_admin/', seguimiento_admin, name='seguimiento_admin'),
    path('reestablecer-password/', reestablecerPassword_admin, name='reestablecerPassword_admin'),
    path('resetear-password/', resetear_contrasena, name='resetear_contrasena')
]