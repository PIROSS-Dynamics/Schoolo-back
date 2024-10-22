from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    subject = models.CharField(max_length=100)  # Ajout de ce champ
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title

