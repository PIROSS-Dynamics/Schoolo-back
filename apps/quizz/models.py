
from django.db import models

class Quizz(models.Model):
    SUBJECT_CHOICES = [
        ('Maths', 'Maths'),
        ('Français', 'Français'),
        ('Anglais', 'Anglais'),
        ('Histoire', 'Histoire'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
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
    order = models.PositiveIntegerField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    correct_answer = models.CharField(max_length=300, blank=True, null=True)  # Pour les questions à réponse écrite

    def __str__(self):
        return f"{self.order}. {self.text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
