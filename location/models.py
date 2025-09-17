from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Configuration(models.Model):
    whatsapp_number = models.CharField(max_length=20, default="25776929167")

    def __str__(self):
        return f"WhatsApp : {self.whatsapp_number}"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"
    
class Lieu(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)

    def __str__(self):
        return self.nom


class Voiture(models.Model):

    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    image = models.ImageField(upload_to='voitures/')
    immatriculation = models.CharField(max_length=20, unique=True)
    disponible = models.BooleanField(default=True)
    prix_par_jour = models.DecimalField(max_digits=10, decimal_places=2)
    lieu_actuel = models.ForeignKey(Lieu, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.immatriculation})"


class Reservation(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, default="En attente")

    def __str__(self):
        return f"Réservation {self.voiture} par {self.client}"

  


