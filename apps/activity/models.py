from django.db import models
from apps.users.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='task_created'  
    )

    def __str__(self):
        return f"Task: {self.title} (Start: {self.start_date}, End: {self.end_date})"