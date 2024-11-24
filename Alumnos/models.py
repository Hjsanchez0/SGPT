from django.db import models
from django.contrib.auth.hashers import is_password_usable, make_password

# Create your models here.
class Alumno(models.Model):
    dni = models.CharField(max_length=8, unique=True)
    codMatricula = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)
    apellidoPat = models.CharField(max_length=30)
    apellidoMat = models.CharField(max_length=30)
    nombres = models.CharField(max_length=70)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    fechaNacimiento = models.DateField()
    domicilio = models.CharField(max_length=100)
    celular = models.CharField(max_length=9)
    email = models.EmailField(max_length=100)
    reset_token = models.CharField(max_length=32, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not is_password_usable(self.password):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

class Proyecto(models.Model):
    institucion = models.CharField(max_length=100)
    ruc = models.CharField(max_length=15)
    titulo = models.CharField(max_length=255)
    director = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=100)

class Tramite(models.Model):
    nombre = models.CharField(max_length=255)

class Carta_Acceso(models.Model):
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE)
    fechaFut = models.DateField()
    estadoFut = models.CharField(max_length=50)
    pdfFut = models.CharField(max_length=255, null=True, blank=True)
    observacionFut = models.CharField(max_length=150)
    fechaCarta = models.DateField(null=True, blank=True)
    pdfCarta = models.CharField(max_length=255, null=True, blank=True)

class Semestre(models.Model):
    semestreAcademico = models.CharField(max_length=10,  null=True, blank=True)

class Proyecto_Alumno(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, null=True, blank=True)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    carta_acceso = models.ForeignKey(Carta_Acceso, on_delete=models.CASCADE, null=True, blank=True)
    dictamenPdf = models.FileField(upload_to='pdfDictamen/', null=True, blank=True)
    notaPromocional = models.IntegerField(null=True, blank=True)