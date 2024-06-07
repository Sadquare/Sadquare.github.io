from django.contrib import admin
from .models import Avion, MaintenanceOperation, MaintenanceHeure, Organes,Material,Besoin,Parachute,Piece,Materiel,Engine
class MaintenanceHeureInline(admin.TabularInline):
    model = MaintenanceHeure

class AvionAdmin(admin.ModelAdmin):
    inlines = [MaintenanceHeureInline]

admin.site.register(Avion, AvionAdmin)
admin.site.register(MaintenanceOperation)
admin.site.register(Organes)
admin.site.register(Material)
admin.site.register(Besoin)
admin.site.register(Parachute)
admin.site.register(Piece)
admin.site.register(Materiel)
admin.site.register(Engine)

