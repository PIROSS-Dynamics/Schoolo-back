# lessons/forms.py
from django import forms
from .models import Lesson, Teacher

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'subject','teacher', 'content', 'is_public','grade']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),  
        }

