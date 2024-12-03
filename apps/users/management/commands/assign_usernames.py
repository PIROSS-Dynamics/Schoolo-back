from django.core.management.base import BaseCommand
from apps.users.models import User
from uuid import uuid4

class Command(BaseCommand):
    help = "Assign unique usernames to users missing one."

    def handle(self, *args, **kwargs):
        users_without_username = User.objects.filter(username__isnull=True)
        for user in users_without_username:
            user.username = f"user_{uuid4().hex[:8]}"
            user.save()
        self.stdout.write(self.style.SUCCESS("Unique usernames assigned to all users without usernames."))
