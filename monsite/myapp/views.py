from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import ConnexionForm
from .models import Avion, MaintenanceHeure, MaintenanceOperation, Organes, Material, Notification,Materiel,Engine

from django.http import HttpResponseRedirect, HttpResponse
from .forms import MaintenanceOperationForm 
from django.db.models import Sum
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from .forms import BesoinForm
from .models import Besoin
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .forms import AjouterHeuresForm
from .models import Parachute
from .models import Piece


def index(request):
    return render(request,'pages/index.html')


from django.http import JsonResponse
from .models import MaintenanceOperation

def get_maintenance_type(request, operation_id):
    try:
        id_op = int(operation_id)
        operation = MaintenanceOperation.objects.get(pk=operation_id)
        maintenance_type = operation.maintenance_type
        return HttpResponse(maintenance_type)
    except MaintenanceOperation.DoesNotExist:
        return JsonResponse({'error': 'Opération non trouvée'}, status=404)



def avions(request):
    return render(request, 'pages/avions.html')

def matériels(request):
    # Récupérer tous les matériaux de la base de données
    materiaux = Material.objects.all()
    
    # Nombre d'éléments par page
    elements_par_page = 10  # Vous pouvez ajuster ce nombre selon vos besoins
    
    # Initialiser le paginateur avec la liste des matériaux et le nombre d'éléments par page
    paginator = Paginator(materiaux, elements_par_page)
    
    # Récupérer le numéro de la page à afficher (par défaut, 1ère page)
    page_numero = request.GET.get('page', 1)
    
    # Obtenir les matériaux pour la page donnée
    page_materiaux = paginator.get_page(page_numero)
    
    # Passer les matériaux paginés au contexte du template
    context = {
        'page_materiaux': page_materiaux,
    }
    return render(request, 'pages/matériels.html', context)


def ajouter_operation(request):
    message = ''
    if request.method == 'POST':
        form = MaintenanceOperationForm(request.POST)
        if form.is_valid():
            form.save()
            message = 'Ajouté avec succès'
        else:
            message = form.errors
    else:
        form = MaintenanceOperationForm()
    return render(request, 'pages/ajouter_operation.html', {'form': form, 'message': message})

from django.shortcuts import render, redirect
from .forms import MaintenanceHeureForm

from .models import MaintenanceHeure

def ajouter_maintenance(request):
    message = ''
    if request.method == 'POST':
        form = MaintenanceHeureForm(request.POST)
        if form.is_valid():
            avion = form.cleaned_data['avion']
            operation = form.cleaned_data['operation']
            heure = form.cleaned_data['heure']
            # Vérifier si une entrée pour cet avion et cette opération existe déjà
            try:
                maintenance_heure = MaintenanceHeure.objects.get(avion=avion, operation=operation)
                # Remplacer l'heure existante par la nouvelle heure
                maintenance_heure.heure = heure
                maintenance_heure.save()
                difference = maintenance_heure.difference()
                print(difference)
        
                if difference is not None and difference <= 100 :
                    # Créer une nouvelle instance de Notification
                    notification = Notification.objects.create(type_notif='Operations', count_type=1)
                message = "Heure mise à jour avec succès."
            except MaintenanceHeure.DoesNotExist:
                # Si aucune entrée n'existe, créer une nouvelle entrée
                form.save()
                message = "Nouvelle heure ajoutée avec succès."
        else:
            message = 'Il y a des erreurs dans le formulaire.'
    else:
        form = MaintenanceHeureForm()
    return render(request, 'pages/ajouter_maintenance.html', {'form': form, 'message': message})

     

def operations_maintenance(request):
    # Récupérer tous les avions et toutes les opérations de maintenance
    avions = Avion.objects.all()
    operations = MaintenanceOperation.objects.all()
    maintenances = MaintenanceHeure.objects.all()
    print(operations)
    from django.db.models import Sum

def operations_maintenance(request):
    avions = Avion.objects.all()
    operations = MaintenanceOperation.objects.all()
    
    # Calculer les heures de vol pour chaque avion
    for avion in avions:
        heures_vol = MaintenanceHeure.objects.filter(avion=avion).aggregate(Sum('heures_vol'))['heures_vol__sum']
        avion.heures_vol = heures_vol if heures_vol else 0
        avion.save()

    context = {
        'avions': avions,
        'operations': operations
    }
    return render(request, 'pages/operations_maintenance.html', context)



def modifier_heure(request):
    if request.method == 'POST':
        avions = Avion.objects.all()
        operations = MaintenanceOperation.objects.all()

        context = {
            'avions': avions,
            'operations': operations
        }
        
        return render(request, 'pages/modifier_heure.html', context)
    
        # Gérer le cas où la méthode est GET
        # Renvoyer le modèle HTML pour afficher le formulaire de modification
    else:
        return render(request, 'pages/modifier_heure.html')

def modifier(request, avion_id):
    if request.method == 'POST':
        form = MaintenanceHeureForm(request.POST)
        if form.is_valid():
            operation = form.cleaned_data['operation']
            avion = form.cleaned_data['avion']
            heure_take = form.cleaned_data['heure'].heure

            modification = MaintenanceHeure.objects.filter(avion=avion, operation=operation)
            heure_ = add_times(modification.first().heure, heure_take)
            # Mettez à jour l'heure de maintenance pour cette opération et cet avion
            modification.update(heure=heure_)
        return render('pages/operations_maintenance.html')  # Rediriger vers la page d'où provient la demande ou vers une autre page
    else:
        # Gérer le cas où la méthode HTTP n'est pas POST
        return render('pages/operations_maintenance.html')  # Rediriger vers la page d'où provient la demande ou vers une autre page
# Create your views here.


def enregistrer_modifications(request):
    if request.method == 'POST':
        for avion in Avion.objects.all():
            for operation in MaintenanceOperation.objects.all():
                champ_name = f"{avion.numero_avion}_{operation.operation_id}"
                heure = request.POST.get(champ_name)
                if heure:
                    # Utilisez get_or_create pour obtenir ou créer l'objet MaintenanceHeure
                    maintenance_heure, _ = MaintenanceHeure.objects.get_or_create(avion=avion, operation=operation)
                    maintenance_heure.heure = heure
                    maintenance_heure.save()
        return redirect('myapp:operations_maintenance')
    return redirect('myapp:operations_maintenance')


# Fonction pour convertir une chaîne au format "hh:mm" en heures et minutes
def convert_to_hours_minutes(time_string):
    hours, minutes = map(int, time_string.split(':'))
    return hours, minutes

# Fonction pour convertir des heures et des minutes en une chaîne au format "hh:mm"
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
"""
time1 = "2:30"
time2 = "1:45"
result = add_times(time1, time2)
"""

def organes_list(request):
    organes = Organes.objects.all()
    return render(request, 'pages/organes_list.html', {'organes': organes})

def ajouter_heure_vol(request):
    from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from django.shortcuts import render, redirect
from .models import Avion
from datetime import datetime


def ajouter_heure_vol(request):
    avions = Avion.objects.all()
    if request.method == 'POST':
        avion_id = request.POST.get('avion_id')
        heures_vol_str = request.POST.get('heures_vol')
        # Obtenir l'objet Avion correspondant
        avion = Avion.objects.get(pk=avion_id)
        avion_heure = avion.heure    

        if avion_heure == "":
            avion_heure = "00:00"
        
        # Extraire les heures et les minutes de l'objet datetime
        heures_vol = add_times(heures_vol_str, avion_heure)
        
        # Mettre à jour l'heure de vol de l'avion
        avion.heure = heures_vol
        avion.save()

        maintenance_heures = MaintenanceHeure.objects.filter(avion=avion)
        for maintenance_heure in maintenance_heures:
                difference = maintenance_heure.difference()
                print(difference)
                if difference is not None and difference <= 100 :
                    notification = Notification.objects.create(type_notif='Operations', count_type=1)
        
        
        
        # Redirection vers une page de confirmation ou une autre page
        return redirect('myapp:operations_maintenance')
    
    # Si la méthode n'est pas POST, renvoyer un formulaire vide
    return render(request, 'pages/ajouter_heure_vol.html', {'avions': avions})

def liste_besoins(request):
    avions = Avion.objects.all()
    return render(request, 'pages/liste_besoins.html', {'avions': avions})

def ajouter_besoin(request):
    if request.method == 'POST':
        form = BesoinForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myapp:liste_besoins')  # Rediriger vers une autre vue après l'enregistrement
    else:
        form = BesoinForm()
    return render(request, 'pages/ajouter_besoin.html', {'form': form})  
def convert_to_minutes(heures_vol_str):
    """
    Convertit une chaîne d'heures de vol au format "hh:mm" en minutes.
    """
    # Séparez les heures et les minutes de la chaîne
    heures, minutes = heures_vol_str.split(':')
    # Convertissez les heures et les minutes en entiers
    heures = int(heures)
    minutes = int(minutes)
    # Convertissez les heures en minutes et ajoutez-les aux minutes
    minutes_totales = heures * 60 + minutes
    return minutes_totales


def ajouter_HDV(request):
    avions = Avion.objects.all()
    if request.method == 'POST':
        avion_numero = request.POST.get('avion_numero')
        heures_vol_str = request.POST.get('heures_vol')
        # Obtenir l'objet Avion correspondant
        organe = Organes.objects.get(numero_avion=avion_numero)
        avion_heure = organe.hdf_actuel

        if avion_heure == "":
            avion_heure = "00:00"
        
        # Extraire les heures et les minutes de l'objet datetime
        heures_vol = add_times(heures_vol_str, avion_heure)
        
        # Mettre à jour l'heure de vol de l'avion
        organe.hdf_actuel = heures_vol
        organe.save()
        differences = organe.differences_hdf_actuel()

        for field, difference in differences.items():
            if difference == 1:
                notification = Notification.objects.create(type_notif='Organes', count_type=1)

        # Redirection vers une page de confirmation ou une autre page
        return redirect('myapp:organes_list')
    
    # Si la méthode n'est pas POST, renvoyer un formulaire vide
    return render(request, 'pages/ajouter_HDV.html', {'avions': avions})

    
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch  # Ajout de l'import pour la constante inch
def print_pdf(request):
    if request.method == 'POST':
        avion_id = request.POST.get('avion_id')
        avion = Avion.objects.get(pk=avion_id)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="besoins_avion_{}.pdf"'.format(avion.numero_avion)

        # Générer le PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        # Ajouter le titre
        title_style = getSampleStyleSheet()['Title']
        title = Paragraph("BESOINS DE L'AVION {}".format(avion.numero_avion), title_style)
        elements.append(title)

        # En-tête du tableau
        data = [['Part Number','Designation', 'Quantité']]

        # Remplir les données du tableau
        for besoin in avion.besoins.all():
            data.append([besoin.materiel.part_number, besoin.materiel.designation, besoin.quantite])

        # Créer le tableau
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        # Ajuster la taille du tableau
        table._argW[0] = 1.5 * inch  # Largeur de la première colonne
        table._argW[1] = 3 * inch    # Largeur de la deuxième colonne
        table._argW[2] = 1.5 * inch  # Largeur de la troisième colonne

        # Ajouter le tableau et le titre au document
        elements.append(table)

        # Construire le document
        doc.build(elements)

        # Renvoyer le PDF en tant que réponse HTTP
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response


    
from django.shortcuts import render, redirect
from .models import Material
from .forms import MaterialForm

def ajouter_materiel(request):
    if request.method == 'POST':
        # Créer une instance de MaterialForm et remplir avec les données du formulaire
        form = MaterialForm(request.POST)
        if form.is_valid():
            # Sauvegarder le nouveau matériau dans la base de données
            form.save()
            # Rediriger vers la page de liste des matériaux après l'ajout réussi
            return redirect('myapp:matériels')
    else:
        # Si la méthode est GET, créer une instance vide de MaterialForm
        form = MaterialForm()
    
    # Passer le formulaire au contexte du template
    context = {
        'form': form
    }
    return render(request, 'pages/ajouter_materiel.html', context)


def afficher_tableau(request):
    parachutes = Parachute.objects.all()
    return render(request, 'pages/parachute.html', {'parachutes': parachutes})


def pieces(request):
    pieces = Piece.objects.all()
    context = {'pieces': pieces}
    return render(request, 'pages/tuyauterie.html', context)

from django.urls import reverse

def admin_panel(request):
    return redirect(reverse('admin:index'))
def befra_info(request):
    # Les informations sur la BEFRA
    befra_info = {
        'localisation': 'Marrakech, Maroc',
        'mission': 'Former les pilotes, les navigateurs et le personnel technique de l\'Armée de l\'Air Royale Marocaine.',
        'formation': 'Formation de pilotes de chasse, de pilotes de transport, de navigateurs aériens, de contrôleurs aériens et de personnel technique pour les avions et les hélicoptères.',
        'equipements_infrastructures': 'Installations modernes avec simulateurs de vol avancés, salles de classe équipées de technologies de pointe, ateliers de maintenance et zones d\'entraînement spécifiques.',
        'cooperation_internationale': 'Relations de coopération avec d\'autres forces aériennes à travers le monde pour échanger des connaissances et participer à des exercices conjoints.',
        'role_strategique': 'Maintien de la capacité opérationnelle et de la préparation au combat de l\'Armée de l\'Air Royale Marocaine, renforcement des liens au sein de la communauté aéronautique.'
    }
    
    return render(request, 'pages/befra_info.html', {'befra_info': befra_info})

def search_materiel(request):
    designation_query = request.GET.get('designation')

    if designation_query:
        materiels = Material.objects.filter(designation__icontains=designation_query)
    else:
        materiels = Material.objects.all()

    context = {'materiels': materiels}
    return render(request, 'pages/search_materiel.html', context)

def tableau_situation_materiel(request):
    materiels = Materiel.objects.all()
    return render(request, 'pages/tableau_situation_materiel.html', {'materiels': materiels})

def engine_list(request):
    engines = Engine.objects.all()
    return render(request, 'pages/engine_list.html', {'engines': engines})
