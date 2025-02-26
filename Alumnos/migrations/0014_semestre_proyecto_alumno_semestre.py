# Generated by Django 5.1.1 on 2024-10-29 06:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumnos', '0013_remove_proyecto_alumno_semestre_delete_semestre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semestre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semestreAcademico', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='proyecto_alumno',
            name='semestre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Alumnos.semestre'),
        ),
    ]
