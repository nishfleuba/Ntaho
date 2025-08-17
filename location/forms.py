from django import forms
from django.contrib.auth.models import User
from .models import Client

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {
            'username': 'Nom d’utilisateur',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
            'password': 'Mot de passe',
        }
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['telephone', 'adresse']        
