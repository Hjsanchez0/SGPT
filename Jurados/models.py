from django.db import models
from django.contrib.auth.hashers import is_password_usable, make_password
from Administrativos.models import Administrativo
from Alumnos.models import Proyecto, Semestre

# Create your models here.
class Rol(models.Model):
    ocupacion = models.CharField(max_length=50)

class Jurado(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    codTrabajador = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    apellidoPat = models.CharField(max_length=30)
    apellidoMat = models.CharField(max_length=30)
    nombres = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    fechaNacimiento = models.DateField()
    domicilio = models.CharField(max_length=150)
    celular = models.CharField(max_length=9)
    email = models.EmailField(max_length=100)
    reset_token = models.CharField(max_length=32, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Asignacion(models.Model):
    administrativo = models.ForeignKey(Administrativo, on_delete=models.SET_NULL, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    jurado = models.ForeignKey(Jurado, on_delete=models.SET_NULL, null=True, blank=True)
    semestre = models.ForeignKey(Semestre, on_delete=models.SET_NULL, null=True, blank=True)
    fechaAsignacion = models.DateField(null=True, blank=True)
    fechaEnvio = models.DateField(null=True, blank=True)
    estadoEnvio = models.CharField(max_length=70, null=True, blank=True)
    drivePdf = models.TextField(null=True, blank=True)
    fechaRevision = models.DateField(null=True, blank=True)
    estadoRevision = models.CharField(max_length=70, null=True, blank=True)
    observacionPdf = models.TextField(null=True, blank=True)
    notaFinal = models.IntegerField(null=True, blank=True)