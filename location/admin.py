from django.contrib import admin
from .models import Client, Lieu, Voiture, Reservation,Configuration


admin.site.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('whatsapp_number',)
    def save_model(self, request, obj, form, change):
        if obj.whatsapp_number:
            # garder uniquement les chiffres
            num = ''.join(filter(str.isdigit, obj.whatsapp_number))

            # enlever les deux premiers 0 si ça commence par 00
            if num.startswith("00"):
                num = num[2:]

            obj.whatsapp_number = num

        super().save_model(request, obj, form, change)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_email', 'telephone', 'adresse']

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Nom complet'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'


@admin.register(Lieu)
class LieuAdmin(admin.ModelAdmin):
    list_display = ('nom', 'adresse')
@admin.register(Voiture)    
class VoitureAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'immatriculation', 'disponible', 'prix_par_jour', 'lieu_actuel')
    readonly_fields = ['image_display']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # voiture déjà existante
            return ['image'] + self.readonly_fields
        return self.readonly_fields

    def image_display(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 200px;">'
        return "Aucune image"
    image_display.allow_tags = True
    image_display.short_description = "Image actuelle"
# @admin.register(Voiture)
# class VoitureAdmin(admin.ModelAdmin):
#     list_display = ('marque', 'modele', 'immatriculation', 'disponible', 'prix_par_jour', 'lieu_actuel')
#     list_filter = ('disponible', 'marque')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client', 'voiture', 'date_debut', 'date_fin', 'statut')
    list_filter = ('statut',)
    search_fields = ('client__username', 'voiture__immatriculation')
