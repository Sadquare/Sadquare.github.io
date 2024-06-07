from django.db import models

# Create your models here.
class utilisateur(models.Model):
    nom=models.CharField(max_length=50)
    mot_de_passe=models.CharField(max_length=50)