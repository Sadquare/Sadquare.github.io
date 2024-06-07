from django.contrib import admin
from django.urls import path
from . import views
from .views import admin_panel
app_name = 'myapp'
urlpatterns = [
    path('index', views.index, name="index"),
    path('avions', views.avions, name='avions'),
    path('matériels', views.matériels, name='matériels'),
    path('operations_maintenance', views.operations_maintenance, name='operations_maintenance'),
    path('modifier', views.modifier_heure, name='modifier'),
    path('enregistrer', views.enregistrer_modifications, name='enregistrer_modifications'),
    path('ajouter_operation', views.ajouter_operation, name='ajouter_operation'),
    path('ajouter_maintenance', views.ajouter_maintenance, name='ajouter_maintenance'),
    path('get_maintenance_type/<int:operation_id>/', views.get_maintenance_type, name='get_maintenance_type'),
    path('organes_list', views.organes_list, name='organes_list'),
    path('ajouter_heure_vol', views.ajouter_heure_vol, name='ajouter_heure_vol'),
    path('ajouter_besoin/', views.ajouter_besoin, name='ajouter_besoin'),
    path('liste_besoins/', views.liste_besoins, name='liste_besoins'),
    path('ajouter_HDV/', views.ajouter_HDV, name='jouter_HDV'),
    path('print_pdf/', views.print_pdf, name='print_pdf'),
    path('ajouter_rechange', views.ajouter_materiel, name='ajouter_materiel'),
    path('parachute', views.afficher_tableau, name='parachute'),
    path('tuyauterie', views.pieces, name='tuyauterie'),
    path('admin/', admin_panel, name='admin_panel'),
    path('befra_info/', views.befra_info, name='befra_info'),
    path('search/', views.search_materiel, name='search_materiel'),
    path('tableau_situation_materiel/', views.tableau_situation_materiel, name='tableau_situation_materiel'),
    path('Engine', views.engine_list, name='engine_list'),
]

