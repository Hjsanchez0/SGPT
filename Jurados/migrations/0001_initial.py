# Generated by Django 5.1.1 on 2024-10-09 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocupacion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Jurado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('codTrabajador', models.CharField(max_length=15, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('apellidoPat', models.CharField(max_length=30)),
                ('apellidoMat', models.CharField(max_length=30)),
                ('nombres', models.CharField(max_length=50)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=1)),
                ('fechaNacimiento', models.DateField()),
                ('domicilio', models.CharField(max_length=150)),
                ('celular', models.CharField(max_length=9)),
                ('email', models.EmailField(max_length=100)),
                ('fk_rol_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Jurados.rol')),
            ],
        ),
    ]
