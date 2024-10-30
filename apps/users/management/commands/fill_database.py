import random
from django.core.management.base import BaseCommand
from faker import Faker
from apps.users.models import Utilisateur, Professeur, Eleve, Parent, Tache, Planning, Speciality, Profil

fake = Faker("fr_FR")

class Command(BaseCommand):
    help = 'Populates the database with random data'

    def handle(self, *args, **kwargs):
        # Create some specialities
        for _ in range(5):
            speciality = Speciality.objects.create(name=fake.job())
        
        # Create some utilisateurs (generic users)
        for _ in range(20):
            # Create a profile first
            profile = Profil.objects.create(
                photo=fake.image_url(),  # You can replace this with any placeholder image URL
                bio=fake.text(max_nb_chars=200)
            )
            
            # Create the user and assign the profile
            user = Utilisateur.objects.create(
                prenom=fake.first_name(),
                nom=fake.last_name(),
                email=fake.email(),
                motDePasse=fake.password(),
                profil=profile  # Associate the profile here
            )

        # Create some professeurs and link specialities
        for _ in range(5):
            # Create a profile for the professor
            profile = Profil.objects.create(
                photo=fake.image_url(),
                bio=fake.text(max_nb_chars=200)
            )
            
            professeur = Professeur.objects.create(
                prenom=fake.first_name(),
                nom=fake.last_name(),
                email=fake.email(),
                motDePasse=fake.password(),
                profil=profile
            )
            professeur.specialities.set(Speciality.objects.order_by('?')[:2])

        # Create some eleves
        for _ in range(10):
            # Create a profile for the eleve
            profile = Profil.objects.create(
                photo=fake.image_url(),
                bio=fake.text(max_nb_chars=200)
            )
            
            eleve = Eleve.objects.create(
                prenom=fake.first_name(),
                nom=fake.last_name(),
                email=fake.email(),
                motDePasse=fake.password(),
                profil=profile,
                niveauExperience=random.randint(1, 5)
            )

        # Create some parents and link children
        for _ in range(5):
            # Create a profile for the parent
            profile = Profil.objects.create(
                photo=fake.image_url(),
                bio=fake.text(max_nb_chars=200)
            )
            
            parent = Parent.objects.create(
                prenom=fake.first_name(),
                nom=fake.last_name(),
                email=fake.email(),
                motDePasse=fake.password(),
                profil=profile
            )
            parent.enfants.set(Eleve.objects.order_by('?')[:2])

        # Create tasks
        for _ in range(10):
            tache = Tache.objects.create(
                nom=fake.sentence(),
                description=fake.paragraph(),
                date_debut=fake.date_time_this_year(),
                date_fin=fake.date_time_this_year()
            )

        # Create planning and add tasks to it
        for _ in range(5):
            planning = Planning.objects.create()
            planning.taches.set(Tache.objects.order_by('?')[:3])

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
