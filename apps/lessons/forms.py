# lessons/forms.py
from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'subject', 'content', 'is_public']

