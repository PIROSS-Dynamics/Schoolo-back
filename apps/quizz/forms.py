
from django import forms
from .models import Quizz, Question, Choice

class QuizzForm(forms.ModelForm):
    class Meta:
        model = Quizz
        fields = ['title', 'subject', 'teacher', 'number_of_questions', 'is_public']  
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'correct_answer']  # Inclure le type de question

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']  # Inclure le choix de réponse
