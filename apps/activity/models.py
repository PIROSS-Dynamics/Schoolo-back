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
    

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'Message'),
        ('relation', 'Relation Request'),
        ('task', 'Task'),
        ('systeme', 'System Notification'),
    ]
    
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=150)
    description = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_sent',
        null=True, blank=True
    )
    
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications_received'
    )
    
    def __str__(self):
        return f"{self.type.capitalize()} Notification: {self.title} to {self.receiver.username} ({'Read' if self.is_read else 'Unread'})"
