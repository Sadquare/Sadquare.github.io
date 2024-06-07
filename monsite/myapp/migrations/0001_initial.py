# Generated by Django 5.0.3 on 2024-04-16 23:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Avion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_avion', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Piece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_piece', models.CharField(max_length=50)),
                ('duree_vie', models.IntegerField(default=365)),
            ],
        ),
        migrations.CreateModel(
            name='LiaisonAvionPiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_pose', models.DateField()),
                ('avion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.avion')),
                ('piece', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.piece')),
            ],
        ),
    ]
