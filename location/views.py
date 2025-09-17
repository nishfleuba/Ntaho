from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import ClientForm,UserForm,ReservationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Configuration

def detail_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    config = Configuration.objects.first()  # tu prends le premier enregistrement

    return render(request, "detail_voiture.html", {
        "voiture": voiture,
        "whatsapp_number": config.whatsapp_number if config else "",
    })


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
    config = Configuration.objects.first()
    whatsapp_number = config.whatsapp_number if config else ""
    return render(request, 'location/voitures.html', {
        'voitures': voitures,
        'whatsapp_number': whatsapp_number
    })

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
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user
            reservation.voiture = voiture
            reservation.save()
            return redirect('mes_reservations')  # tu rediriges vers la page "mes réservations"
    else:
        form = ReservationForm()
    return render(request, 'location/reservation_form.html', {'form': form, 'voiture': voiture})

@login_required
def mes_reservations(request):
    # logiques pour afficher les réservations de l'utilisateur connecté
    return render(request, "location/mes_reservations.html")

def connexion(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("accueil")  # ✅ redirige vers accueil
        else:
            return render(request, "connexion.html", {
                "error": "Nom d'utilisateur ou mot de passe incorrect."
            })
    return render(request, "inscription.html")