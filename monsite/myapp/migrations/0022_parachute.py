# Generated by Django 5.0.3 on 2024-05-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_remove_organes_avion_remove_organes_heures_vol_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parachute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField(unique=True)),
                ('prochaine_inspection', models.CharField(max_length=100)),
            ],
        ),
    ]