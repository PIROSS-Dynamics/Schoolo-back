from django.db import models
from apps.users.models import User
from apps.quizz.models import Quizz

class QuizzResult(models.Model):
    score = models.FloatField() 
    total = models.FloatField()  
    date = models.DateTimeField(auto_now_add=True)  

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    
    quizz = models.ForeignKey(
        Quizz,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Quizz: {self.quizz.subject}, User: {self.user}, Score: {self.score} (Date: {self.date})"
    
    
class Challenge(models.Model):
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"User: {self.user}, Score: {self.score} (Date: {self.date})"

class GuessWordResult(Challenge):
    pass

class FindCountryResult(Challenge):
    pass