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

    GRADE_CHOICES = [
        (1, 'CP'),
        (2, 'CE1'),
        (3, 'CE2'),
        (4, 'CM1'),
        (5, 'CM2'),
    ]

    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    content = models.TextField()
    is_public = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    grade = models.IntegerField(choices=GRADE_CHOICES, default=1)  
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title
