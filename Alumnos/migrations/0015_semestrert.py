# Generated by Django 5.1.1 on 2024-10-29 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumnos', '0014_semestre_proyecto_alumno_semestre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Semestrert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semestreAcademico', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]
