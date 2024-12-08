from django import forms 
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label="Password Confirmation",widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ["username","email","first_name","last_name","bio"]
    
    def clean_password_confirmation(self): # c'est pour vérifier que les 2 passwords saisis sont égaux
        pass1 = self.cleaned_data["password"]
        pass2 = self.cleaned_data["password_confirmation"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Véifier le saisis de vos mots de passes.")
        return pass2
        
    def save(self, commit =True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        
        
        
        
        
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href='../password'>Pour changer le mot de passe, clicker ici.</a>") # ca permet de voir le password haché, dans le panneau admin
    class Meta:
        model= CustomUser
        fields = ["username","email","first_name","last_name","is_active","is_admin"]

    def clean_password_confirmation(self): # c'est pour vérifier que les 2 passwords saisis sont égaux
        pass1 = self.cleaned_data["password"]
        pass2 = self.cleaned_data["password_confirmation"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Véifier le saisie de vos mots de passes.")
        return pass2
        

    
class RegisterUserForm(ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label="Password Confirmation",widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username','email']
        
    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError("Les mots de passes sasies ne se correspondent pas.")




