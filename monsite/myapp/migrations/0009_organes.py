# Generated by Django 5.0.3 on 2024-04-29 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_maintenanceheure_heure'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_avion', models.CharField(max_length=10)),
                ('helice_5ans', models.DateField(blank=True, null=True)),
                ('reg_helice_5ans', models.DateField(blank=True, null=True)),
                ('accu_vol_dos_5ans', models.DateField(blank=True, null=True)),
                ('magnetos_D_2000h', models.CharField(blank=True, max_length=10, null=True)),
                ('magnetos_G_2000h', models.CharField(blank=True, max_length=10, null=True)),
                ('fuel_pump_2000h', models.CharField(blank=True, max_length=10, null=True)),
                ('fuel_injecter_1600h', models.CharField(blank=True, max_length=10, null=True)),
                ('hdf_actuel', models.CharField(blank=True, max_length=10, null=True)),
            ],
        ),
    ]