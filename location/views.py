from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import ClientForm,UserForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def accueil(request):
    voitures = Voiture.objects.all()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = ClientForm(request.POST)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Hash du mot de passe
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            return redirect('accueil')  # ou login ou autre

    else:
        user_form = UserForm()
        client_form = ClientForm()

    return render(request, 'location/accueil.html', {
        'voitures': voitures,
        'user_form': user_form,
        'client_form': client_form
    })

def voitures_view(request):
    voitures = Voiture.objects.all()
    return render(request, 'location/voitures.html', {'voitures': voitures})

def inscription_client(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = ClientForm(request.POST)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            return redirect('accueil')
    else:
        user_form = UserForm()
        client_form = ClientForm()

    return render(request, 'location/inscription.html', {
        'user_form': user_form,
        'client_form': client_form
    })
def Apropos(request):
    return render(request, 'location/apropos.html')

@login_required
def reserver_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    client = get_object_or_404(Client, user=request.user)
    lieux = Lieu.objects.all()  # Pour choisir le lieu de départ et retour

    if request.method == 'POST':
        lieu_depart_id = request.POST.get('lieu_depart')
        lieu_retour_id = request.POST.get('lieu_retour')
        lieu_depart = get_object_or_404(Lieu, id=lieu_depart_id)
        lieu_retour = get_object_or_404(Lieu, id=lieu_retour_id)

        Reservation.objects.create(
            client=client,
            voiture=voiture,
            lieu_depart=lieu_depart,
            lieu_retour=lieu_retour,
            date_reservation=timezone.now(),
            est_confirmee=False  # ou True si tu veux confirmer immédiatement
        )
        return redirect('liste_voitures')  # ou vers une page de confirmation

    return render(request, 'reserver_voiture.html', {
        'voiture': voiture,
        'lieux': lieux
    })