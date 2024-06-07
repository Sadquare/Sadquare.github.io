from django.db import models
from django.utils import timezone
from datetime import datetime


class Avion(models.Model):
    numero_avion = models.CharField(max_length=50, unique=True)
    heures_vol = models.IntegerField(default=0)  # Champ pour stocker les heures de vol de l'avion
    heure = models.CharField(max_length=255, default="00:00")
    def __str__(self):
        return self.numero_avion
    
    def get_heure_for_operation(self, operation_id):
        try:
            maintenance_heure = self.maintenanceheure_set.get(operation_id=operation_id)
            return maintenance_heure.heure
        except MaintenanceHeure.DoesNotExist:
            return ""  # Retourner une chaîne vide si aucune heure n'est trouvée pour l'opération donnée

    

class MaintenanceOperation(models.Model):
    TYPE_CHOICES = [
        ('horaire', 'horaire'),
        ('calendaire', 'calendaire')
    ]
    nom = models.CharField(max_length=50)
    duree_limite=models.IntegerField(default=0)
    date_limite=models.DateField(default=timezone.now)
    maintenance_type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='horaire')
    
    def __str__(self):
        return self.nom


class MaintenanceHeure(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    operation = models.ForeignKey(MaintenanceOperation, on_delete=models.CASCADE)
    heure = models.CharField(max_length=255, default="")
    date_initial = models.DateField(default=timezone.now)  # Définition de la valeur par défaut à la date actuelle
    heures_vol = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.avion} - {self.operation} - {self.date_initial}- {self.heure}"
    
    def convert_to_hours_minutes(self, time_string):
        hours, minutes = map(int, time_string.split(':'))
        total_minute = hours*60 + minutes
        return total_minute
    
    def difference(self):
        try:
            heure_avion =self.convert_to_hours_minutes(self.avion.heure)
            heure_maintenance = self.convert_to_hours_minutes(self.heure)
            difference = heure_maintenance - heure_avion

            diff_final = difference // 60

        except:
            diff_final = 0
        return diff_final


class Organes(models.Model):
    numero_avion = models.CharField(max_length=10, null=True)
    heure = models.CharField(max_length=255, default="00:00")
    helice_5ans = models.CharField(max_length=10, null=True, blank=True)
    reg_helice_5ans = models.CharField(max_length=10, null=True, blank=True)
    accu_vol_dos_5ans = models.CharField(max_length=10, null=True, blank=True)
    Moteur_12ans = models.CharField(max_length=10, null=True, blank=True)
    magnetos_D_2000h = models.CharField(max_length=10, null=True, blank=True)
    magnetos_G_2000h = models.CharField(max_length=10, null=True, blank=True)
    fuel_pump_2000h = models.CharField(max_length=10, null=True, blank=True)
    fuel_injecter_1600h = models.CharField(max_length=10, null=True, blank=True)
    hdf_actuel = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Avion {self.numero_avion}"
    

    def convert_to_hours_minutes(self, time_string):
        hours, minutes = map(int, time_string.split(':'))
        total_minute = hours*60 + minutes
        return total_minute

    def difference_dates(self, date_str):
    # Convertir la chaîne de caractères en objet datetime
        date_format = "%d/%m/%y"
        date = datetime.strptime(date_str, date_format)
        
        # Obtenir la date d'aujourd'hui
        today = datetime.now()
        
        # Calculer la différence entre les deux dates
        difference = date - today
        
        # Retourner la différence en jours
        return int(difference.days)
    
    def return_hr(self, field_name):
        hdf_actuel_value = self.hdf_actuel
        field_value = str(getattr(self, field_name, "0"))
        difference = self.convert_to_hours_minutes(field_value) - self.convert_to_hours_minutes(hdf_actuel_value)
        diff = difference // 60 
        if diff < 100:
            return 1
        else:
            return 0
    def return_mt(self, field_name):
        field_value = str(getattr(self, field_name, "0"))
        diff_days = self.difference_dates(field_value)
        if diff_days < 365:
            return 1
        else:
            return 0
    
    def differences_hdf_actuel(self):
        differences = {}

        differences['helice_5ans'] = self.return_mt('helice_5ans')
        differences['reg_helice_5ans'] = self.return_mt('reg_helice_5ans')
        differences['accu_vol_dos_5ans'] = self.return_mt('accu_vol_dos_5ans')

        differences['magnetos_D_2000h'] = self.return_hr('magnetos_D_2000h')
        differences['magnetos_G_2000h'] = self.return_hr('magnetos_G_2000h')
        differences['fuel_pump_2000h'] = self.return_hr('fuel_pump_2000h')
        differences['fuel_injecter_1600h'] = self.return_hr('fuel_injecter_1600h')

        return differences



class Material(models.Model):
    part_number = models.CharField(max_length=100, unique=True)
    designation = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    quantity = models.IntegerField()
    support = models.CharField(max_length=100)

    def __str__(self):
        return self.part_number


class Besoin(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE, related_name="besoins")
    materiel = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="besoins")
    quantite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.avion} - {self.materiel} - Quantité: {self.quantite}"
    
class Notification(models.Model):
    type_notif = models.CharField(max_length=50, choices=[('Organes', 'Organes'),('Operations', 'Operations')])
    count_type = models.IntegerField(default=1)

class Parachute(models.Model):
    numero = models.IntegerField(unique=True)
    prochaine_inspection = models.CharField(max_length=100)

    def __str__(self):
        return str(self.numero)

class Piece(models.Model):
    designation = models.CharField(max_length=100)
    pn = models.CharField(max_length=100)
    limite_calendaire = models.CharField(max_length=100)
    obs = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.designation
    

class Materiel(models.Model):
    part_number = models.CharField(max_length=50, default='')
    designation = models.CharField(max_length=100, default='')
    Serial_number = models.CharField(max_length=50, default='')
    avionnee = models.CharField(max_length=1, choices=[('X', 'X'), ('', '')], default='', blank=True)
    ste = models.CharField(max_length=1, choices=[('X', 'X'), ('', '')], default='', blank=True)
    basg = models.CharField(max_length=1, choices=[('X', 'X'), ('', '')], default='', blank=True)
    dispo_unite = models.CharField(max_length=1, choices=[('X', 'X'), ('', '')], default='', blank=True)
    indispo_unite = models.CharField(max_length=1, choices=[('X', 'X'), ('', '')], default='', blank=True)

    def __str__(self): 
        return self.part_number

class Engine(models.Model):
    av_number = models.CharField(max_length=10)
    engine_number = models.CharField(max_length=20)
    tso = models.CharField(max_length=20)
    tsn = models.CharField(max_length=20)
    next_rg_date = models.DateField(null=True, blank=True)
    observation = models.TextField(blank=True)

    def __str__(self):
        return self.av_number
    
