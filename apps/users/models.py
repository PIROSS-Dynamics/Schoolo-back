from django.db import models

        # -- Tache
class Tache(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    def __str__(self):
        return f"Tâche: {self.nom} (Début: {self.date_debut}, Fin: {self.date_fin})"



        # -- Planning
class Planning(models.Model):
    taches = models.ManyToManyField(Tache)

    def __str__(self):
        return f"Planning avec {self.taches.count()} tâche(s)"



        # -- Profil
class Profil(models.Model):
    photo = models.CharField(max_length=200)
    bio = models.TextField()

    def __str__(self):
        return f"Profil (Photo: {self.photo}, Bio: {self.bio[:30]}...)"




        # -- Utilisateur
class Utilisateur(models.Model):
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    motDePasse = models.CharField(max_length=50)
    planning = models.ForeignKey(Planning, on_delete=models.SET_NULL, null=True)
    profil = models.OneToOneField(Profil, on_delete=models.CASCADE)

    def __str__(self):
        return f"Utilisateur: {self.prenom} {self.nom} (Email: {self.email})"



        # -- Eleve
class Eleve(Utilisateur):
    niveauExperience = models.IntegerField(default=0)

    def __str__(self):
        return f"Élève: {self.prenom} {self.nom} - Niveau: {self.niveauExperience}"



        # -- Specilité (Specilaity)
class Speciality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Spécialité: {self.name}"



        # -- Professeur
class Professeur(Utilisateur):
    specialities = models.ManyToManyField(Speciality, blank=True)

    def __str__(self):
        specialities_list = ", ".join([s.name for s in self.specialities.all()])
        return f"Professeur: {self.prenom} {self.nom} - Spécialités: {specialities_list or 'Aucune'}"



        # -- Parent
class Parent(Utilisateur):
    enfants = models.ManyToManyField(Eleve)

    def __str__(self):
        enfants_list = ", ".join([f"{enfant.prenom} {enfant.nom}" for enfant in self.enfants.all()])
        return f"Parent: {self.prenom} {self.nom} - Enfants: {enfants_list or 'Aucun'}"



        # -- Lecon
class Lecon(models.Model):
    titre = models.CharField(max_length=100)
    contenu = models.CharField(max_length=255)
    matiere = models.CharField(max_length=100)
    estPublic = models.BooleanField(default=False)
    professeur = models.ForeignKey(Professeur, on_delete=models.CASCADE)

    def __str__(self):
        return f"Leçon: {self.titre} (Matière: {self.matiere}, Public: {'Oui' if self.estPublic else 'Non'})"
