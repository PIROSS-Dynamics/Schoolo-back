
from django.db import models

class Lesson(models.Model):
    SUBJECT_CHOICES = [
        ('Maths', 'Maths'),
        ('Français', 'Français'),
        ('Anglais', 'Anglais'),
        ('Histoire', 'Histoire'),
    ]

    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)  # Utiliser les choix
    content = models.TextField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title


