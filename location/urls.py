from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),  
    path('voitures/', views.voitures_view, name='liste_voitures'),
    # path('inscription/', inscription_client.as_view(), name='inscription'),
    path('inscription/', views.inscription_client, name='inscription'),
    path('apropos/', views.Apropos, name='apropos'), 
    path("reserver/<int:voiture_id>/", views.reserver_voiture, name="reserver_voiture"),
    path("mes_reservations/", views.mes_reservations, name="mes_reservations"),
    path("connexion/", views.connexion, name="connexion"),

]
