# Generated by Django 5.1.1 on 2024-10-18 03:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumnos', '0004_alter_proyecto_alumno_notapromocional_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto_alumno',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alumnos_proyecto', to='Alumnos.proyecto'),
        ),
    ]
