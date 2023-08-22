from django.db import models
from django_countries.fields import CountryField

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    firm = models.CharField(max_length=50, verbose_name="Raison Sociale")
    first_name = models.CharField(max_length=50, verbose_name="Prénom")
    last_name = models.CharField(max_length=50, verbose_name="Nom")
    email = models.CharField(max_length=100, verbose_name="Email")
    phone = models.CharField(max_length=15, verbose_name="Téléphone")
    address = models.CharField(max_length=100, verbose_name="Adresse")
    city = models.CharField(max_length=50, verbose_name="Ville")
    country = CountryField(blank_label='(Choisir Pays)',  verbose_name="Pays",)
    zipcode = models.CharField(max_length=20, verbose_name="BP", blank=True, null=True)

    def __str__(self):
        return (f"{self.first_name} ({self.firm})")
