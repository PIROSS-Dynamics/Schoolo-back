from django.contrib import admin
from .models import Tache, Planning, Profil, Utilisateur, Eleve, Speciality, Professeur, Parent, Lecon

@admin.register(Tache)
class TacheAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'date_debut', 'date_fin')
    search_fields = ('nom', 'description')
    list_filter = ('date_debut', 'date_fin')

@admin.register(Planning)
class PlanningAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_taches')
    
    def get_taches(self, obj):
        return ", ".join([tache.nom for tache in obj.taches.all()])
    get_taches.short_description = 'Tâches'

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'bio')

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'planning', 'profil')
    search_fields = ('prenom', 'nom', 'email')
    list_filter = ('planning',)

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'niveauExperience')
    search_fields = ('prenom', 'nom')
    list_filter = ('niveauExperience',)

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Professeur)
class ProfesseurAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'get_specialities')
    search_fields = ('prenom', 'nom')
    
    def get_specialities(self, obj):
        return ", ".join([speciality.name for speciality in obj.specialities.all()])
    get_specialities.short_description = 'Spécialités'

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'get_enfants')
    search_fields = ('prenom', 'nom')
    
    def get_enfants(self, obj):
        return ", ".join([f"{enfant.prenom} {enfant.nom}" for enfant in obj.enfants.all()])
    get_enfants.short_description = 'Enfants'

@admin.register(Lecon)
class LeconAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'estPublic', 'professeur')
    search_fields = ('titlsre', 'matiere')
    list_filter = ('estPublic', 'matiere')
