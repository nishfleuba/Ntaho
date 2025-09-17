from django import forms
from django.contrib.auth.models import User
from .models import Client,Reservation

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['telephone', 'adresse'] 
        


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_debut', 'date_fin']
               
