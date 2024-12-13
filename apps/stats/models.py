from django.db import models
from apps.users.models import User
from apps.quizz.models import Quizz

class QuizzResult(models.Model):
    score = models.CharField(max_length=100)
    date = models.DateTimeField()
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    quizz = models.ForeignKey(
        Quizz,
        on_delete=models.CASCADE,
    )


    def __str__(self):
        return f"Quizz: {self.quizz} User: {self.user}, Score: {self.score} (Date: {self.date})"