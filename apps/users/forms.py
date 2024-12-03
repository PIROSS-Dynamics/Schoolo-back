from django import forms 
from .models import Student


class StudentSignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'photo', 'bio', 'experience_level']
        widgets ={
            'password' : forms.PasswordInput(),
        }