# Generated by Django 5.1.1 on 2024-11-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumnos', '0020_proyecto_alumno_dictamenpdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto_alumno',
            name='dictamenPdf',
            field=models.FileField(blank=True, null=True, upload_to='pdfDictamen/'),
        ),
    ]
