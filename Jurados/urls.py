from django.urls import path
from .views import jurado_login, dashboard_jurado, datosPersonales_jurado, actualizarDatos_jurado, changePassword_jurado, evaluacion_jurado, evaluacion_jurado_proyecto, guardar_evaluacion, logout_view, reestablecerPassword_jurado, resetear_contrasena

#Create your urls here.
urlpatterns = [
    path('login/', jurado_login, name='jurado_login'),
    path('dashboard/', dashboard_jurado, name='dashboard_jurado'),
    path('logout/', logout_view, name='logout'),
    path('datospersonales/', datosPersonales_jurado, name='datosPersonales_jurado'),
    path('datospersonales/actualizar-datos/', actualizarDatos_jurado, name='actualizarDatos_jurado'),
    path('datospersonales/changepassword/', changePassword_jurado, name='changePassword_jurado'),
    path('evaluacion/', evaluacion_jurado, name='evaluacion_jurado'),
    path('evaluacion/evaluacion_proyecto/<int:asignacion_id>/', evaluacion_jurado_proyecto, name='evaluacion_jurado_proyecto'),
    path('evaluacion/guardar-evaluacion/', guardar_evaluacion, name='guardar_evaluacion'),
    path('reestablecer-password/', reestablecerPassword_jurado, name='reestablecerPassword_jurado'),
    path('resetear-password/', resetear_contrasena, name='resetear_contrasena')
]