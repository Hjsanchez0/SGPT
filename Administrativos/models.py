from django.db import models
from django.contrib.auth.hashers import is_password_usable, make_password

# Create your models here.
class Administrativo(models.Model):
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

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)