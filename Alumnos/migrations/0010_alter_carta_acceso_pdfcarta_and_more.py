# Generated by Django 5.1.1 on 2024-10-23 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alumnos', '0009_alter_carta_acceso_pdfcarta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carta_acceso',
            name='pdfCarta',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='carta_acceso',
            name='pdfFut',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
