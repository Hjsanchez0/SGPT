# Generated by Django 5.1.1 on 2024-10-30 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administrativos', '0003_alter_asignacion_jurado_alter_asignacion_notafinal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacion',
            name='administrativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Administrativos.administrativo'),
        ),
    ]
