# Generated by Django 5.1.3 on 2024-12-10 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appWeb', '0009_alter_horatomada_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='horatomada',
            options={'verbose_name': 'Hora Tomada', 'verbose_name_plural': 'Horas Tomadas'},
        ),
        migrations.AddField(
            model_name='horatomada',
            name='enfermedad',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Enfermedad'),
        ),
        migrations.AddField(
            model_name='horatomada',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento'),
        ),
        migrations.AddField(
            model_name='horatomada',
            name='materno',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apellido Materno'),
        ),
        migrations.AddField(
            model_name='horatomada',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='horatomada',
            name='paterno',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apellido Paterno'),
        ),
        migrations.AddField(
            model_name='horatomada',
            name='sexo',
            field=models.CharField(blank=True, choices=[('m', 'Masculino'), ('f', 'Femenino'), ('o', 'Otro')], max_length=1, null=True, verbose_name='Sexo'),
        ),
        migrations.AlterField(
            model_name='horatomada',
            name='especialidad',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Especialidad'),
        ),
        migrations.AlterField(
            model_name='horatomada',
            name='lugar_de_atencion',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Lugar de Atención'),
        ),
        migrations.AlterField(
            model_name='horatomada',
            name='medico',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Médico'),
        ),
        migrations.AlterModelTable(
            name='horatomada',
            table='hora_tomada',
        ),
    ]
