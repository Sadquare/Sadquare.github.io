# forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import MaintenanceOperation, MaintenanceHeure
from .models import Besoin, Organes
from .models import Material

class ConnexionForm(AuthenticationForm):
    # Vous pouvez personnaliser les champs du formulaire si nécessaire
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)



class MaintenanceOperationForm(forms.ModelForm):
    class Meta:
        model = MaintenanceOperation
        fields = ['nom','duree_limite','date_limite','maintenance_type']


class MaintenanceHeureForm(forms.ModelForm):
    class Meta:
        model = MaintenanceHeure
        fields = ['avion', 'operation','heure', 'date_initial',]


class BesoinForm(forms.ModelForm):
    class Meta:
        model = Besoin
        fields = ['avion', 'materiel', 'quantite']

class AjouterHeuresForm(forms.Form):
    numero_avion = forms.ModelChoiceField(queryset=Organes.objects.all(), label='Choisir l\'avion')
    heures_vol = forms.CharField(label='Heures de vol (hh:mm)')

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['part_number', 'designation', 'unit', 'quantity', 'support']

