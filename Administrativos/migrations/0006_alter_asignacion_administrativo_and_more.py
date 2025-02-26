# Generated by Django 5.1.1 on 2024-10-30 16:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrativos', '0005_asignacion_semestre'),
        ('Alumnos', '0018_proyecto_cargo'),
        ('Jurados', '0002_rename_fk_rol_id_jurado_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacion',
            name='administrativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Administrativos.administrativo'),
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='jurado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Jurados.jurado'),
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='semestre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Alumnos.semestre'),
        ),
    ]
