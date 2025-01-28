
from django.db import models
from apps.users.models import Teacher


class Lesson(models.Model):
    SUBJECT_CHOICES = [
        ('Maths', 'Maths'),
        ('Français', 'Français'),
        ('Anglais', 'Anglais'),
        ('Histoire', 'Histoire'),
        ('Art', 'Art'),
    ]

    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)  # Utiliser les choix
    teacher = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True)
    
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


