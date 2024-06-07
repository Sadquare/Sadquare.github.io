# Generated by Django 5.0.3 on 2024-04-24 02:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_maintenanceheure_heure'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenanceheure',
            name='date_initial',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='maintenanceoperation',
            name='date_limite',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='maintenanceoperation',
            name='duree_limite',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='maintenanceoperation',
            name='maintenance_type',
            field=models.CharField(choices=[('horaire', 'horaire'), ('calendaire', 'calendaire')], default='horaire', max_length=100),
        ),
        migrations.AlterField(
            model_name='maintenanceheure',
            name='heure',
            field=models.IntegerField(),
        ),
    ]
