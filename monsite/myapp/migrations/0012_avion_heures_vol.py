# Generated by Django 5.0.3 on 2024-04-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_maintenanceheure_heures_vol'),
    ]

    operations = [
        migrations.AddField(
            model_name='avion',
            name='heures_vol',
            field=models.IntegerField(default=0),
        ),
    ]
