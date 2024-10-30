import random
from django.core.management.base import BaseCommand
from faker import Faker
from apps.users.models import User, Teacher, Student, Parent, Task, Schedule, Profile

fake = Faker("fr_FR")

class Command(BaseCommand):
    help = 'Populates the database with random data'

    def handle(self, *args, **kwargs):
        # Create some profiles
        for _ in range(20):
            profile = Profile.objects.create(
                photo=fake.image_url(),
                bio=fake.text(max_nb_chars=200)
            )
            
            # Create the user and assign the profile
            user = User.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password(),
                profile=profile  # Associate the profile here
            )

        # Create some teachers
        for _ in range(5):
            profile = Profile.objects.create(
                photo=fake.image_url(),
                bio=fake.text(max_nb_chars=200)
            )
            
            teacher = Teacher.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password(),
                profile=profile
            )

        # Create some students
        for _ in range(10):
            profile = Profile.objects.create(
                photo=fake.image_url(),
                bio=fake.text(max_nb_chars=200)
            )
            
            student = Student.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password(),
                profile=profile,
                experience_level=random.randint(1, 5)
            )

        # Create some parents and link children
        for _ in range(5):
            profile = Profile.objects.create(
                photo=fake.image_url(),
                bio=fake.text(max_nb_chars=200)
            )
            
            parent = Parent.objects.create(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password(),
                profile=profile
            )
            parent.children.set(Student.objects.order_by('?')[:2])

        # Create tasks
        for _ in range(10):
            task = Task.objects.create(
                name=fake.sentence(),
                description=fake.paragraph(),
                start_date=fake.date_time_this_year(),
                end_date=fake.date_time_this_year()
            )

        # Create schedules and add tasks to them
        for _ in range(5):
            schedule = Schedule.objects.create()
            schedule.tasks.set(Task.objects.order_by('?')[:3])

        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
