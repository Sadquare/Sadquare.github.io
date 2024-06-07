# Generated by Django 5.0.3 on 2024-05-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organes',
            name='Moteur_12ans',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='accu_vol_dos_5ans',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='fuel_injecter_1600h',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='fuel_pump_2000h',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='hdf_actuel',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='helice_5ans',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='magnetos_D_2000h',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='magnetos_G_2000h',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='numero_avion',
        ),
        migrations.RemoveField(
            model_name='organes',
            name='reg_helice_5ans',
        ),
        migrations.AddField(
            model_name='organes',
            name='avion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='organes',
            name='heures_vol',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organes',
            name='operation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='organes',
            name='heure',
            field=models.CharField(default='', max_length=255),
        ),
    ]
