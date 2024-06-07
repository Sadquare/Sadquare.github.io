# 1. Configurer Django
import os, datetime
import django, csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')
django.setup()

# 2. Importer les modèles Django
from myapp.models import MaintenanceHeure, Avion, MaintenanceOperation, Material

# 3. Effectuer des opérations sur les modèles Django
# Exemple : Lire tous les enregistrements de MonModele

from myapp.models import Organes, Avion

def g_date(date_str):
    return datetime.datetime.strptime(date_str, "%d/%m/%y").date()

# Chemin vers votre fichier CSV
chemin_fichier_csv = 'db_organes.csv'

# Ouvrir le fichier CSV et lire son contenu
with open(chemin_fichier_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    # Lire chaque ligne du fichier CSV
    i=0
    for row in zip(*csvreader):
        i+=1
        numero_avion = row[0]
        # Ignorer la première ligne (entêtes)
        
        if i == 1 or numero_avion == '':
            continue
        else:
        
            avion, created = Avion.objects.get_or_create(numero_avion=numero_avion)
            try:
                organe, created = Organes.objects.get_or_create(numero_avion=avion, accu_vol_dos_5ans=row[3], fuel_injecter_1600h=row[7], fuel_pump_2000h=row[6], hdf_actuel=row[8], helice_5ans=row[1], magnetos_D_2000h=row[4], magnetos_G_2000h=row[5], reg_helice_5ans=row[2])
            except Organes.DoesNotExist:
                pass  # Ignorer si l'organe n'existe pas dans le modèle"""

"""def importer_donnees_csv(chemin_fichier):
    with open(chemin_fichier, 'r') as fichier_csv:
        lecteur_csv = csv.DictReader(fichier_csv)
        noms_champs = lecteur_csv.fieldnames
        (pn, dsg, unit, qt, sprt) = (noms_champs[0], noms_champs[1], noms_champs[2], noms_champs[3], noms_champs[4])
        i=1
        for ligne in lecteur_csv:
            
            # Créer une instance de votre modèle avec les données de la ligne CSV
            
            nouvel_objet = Material(
                part_number=ligne[pn],
                designation=ligne[dsg],
                unit=ligne[unit],
                quantity=ligne[qt],
                support=ligne[sprt]
            )
            # Enregistrer l'objet dans la base de données
            try:
                nouvel_objet.save()
            except:
                continue

importer_donnees_csv('db_matériels.csv')"""
