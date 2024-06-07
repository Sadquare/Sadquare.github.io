# Fonction pour convertir des heures et des minutes en une chaîne au format "hh:mm"
# Fonction pour convertir une chaîne au format "hh:mm" en heures et minutes
def convert_to_hours_minutes(time_string):
    hours, minutes = map(int, time_string.split(':'))
    return hours, minutes

def convert_to_time_string(hours, minutes):
    return f"{hours:02d}:{minutes:02d}"

# Fonction pour ajouter deux heures ensemble
def add_times(time1, time2):
    hours1, minutes1 = convert_to_hours_minutes(time1)
    hours2, minutes2 = convert_to_hours_minutes(time2)
    
    total_minutes = minutes1 + minutes2
    total_hours = hours1 + hours2 + total_minutes // 60
    total_minutes %= 60
    
    return convert_to_time_string(total_hours, total_minutes)

# Exemple d'utilisation
time1 = "1200:15"
time2 = "1:45"
result = add_times(time1, time2)
print(result)  # Output: 4:15
