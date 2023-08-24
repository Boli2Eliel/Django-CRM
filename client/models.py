from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField

from authentication.models import Account


class Client(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Account, related_name='clients', on_delete=models.CASCADE, verbose_name='Créé par')
    firm = models.CharField(max_length=50, verbose_name="Raison Sociale")
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    email = models.CharField(max_length=100, verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Téléphone")
    address = models.CharField(max_length=100, verbose_name="Adresse")
    zipcode = models.CharField(max_length=20, verbose_name="BP", blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="Ville")
    country = CountryField(blank_label='(Choisir Pays)', verbose_name="Pays", )
    converted_date = models.DateTimeField(null=True, blank=True, verbose_name="Date_conversion_en_client")

    def __str__(self):
        return (f"{self.first_name} ({self.firm})")
