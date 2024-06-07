from datetime import datetime
def difference_dates(date_str):
    # Convertir la chaîne de caractères en objet datetime
        date_format = "%d/%m/%y"
        date = datetime.strptime(date_str, date_format)
        
        # Obtenir la date d'aujourd'hui
        today = datetime.now()
        
        # Calculer la différence entre les deux dates
        difference = today - date
        
        # Retourner la différence en jours
        return int(difference.days)

print(difference_dates('22/06/06'))