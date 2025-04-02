
from django import forms
from .models import Quizz, Question, Choice

class QuizzForm(forms.ModelForm):
    class Meta:
        model = Quizz
        fields = ['title', 'subject', 'teacher', 'number_of_questions', 'is_public', 'grade']  
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'correct_answer'] 

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']  
