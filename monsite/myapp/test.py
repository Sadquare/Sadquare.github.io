# 1. Configurer Django
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monsite.settings')
django.setup()

# 2. Importer les modèles Django
from models import MaintenanceHeure

# 3. Effectuer des opérations sur les modèles Django
# Exemple : Lire tous les enregistrements de MonModele
enregistrements = MaintenanceHeure.objects.all()
for enregistrement in enregistrements:
    print(enregistrement)

# Chemin vers votre fichier CSV
chemin_fichier_csv = 'db.csv'
"""
# Ouvrir le fichier CSV et lire son contenu
with open(chemin_fichier_csv, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    # Transposer les données (convertir les lignes en colonnes)
    transposed_data = zip(*csvreader)
    # Afficher chaque colonne
    for column in transposed_data:
        print(column)
"""
