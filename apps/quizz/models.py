
from django.db import models
from apps.users.models import Teacher


class Quizz(models.Model):
    SUBJECT_CHOICES = [
        ('Maths', 'Maths'),
        ('Français', 'Français'),
        ('Anglais', 'Anglais'),
        ('Histoire', 'Histoire'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='quizzes')
    number_of_questions = models.PositiveIntegerField()
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPES = [
        ('text', 'Text'),        # Réponse écrite
        ('choice', 'Choice'),    # Choix multiple
    ]

    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    correct_answer = models.CharField(max_length=300, blank=True, null=True)  # Pour les questions à réponse écrite

    def __str__(self):
        return self.text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=300)


    def __str__(self):
        return self.text
