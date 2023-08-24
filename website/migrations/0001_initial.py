# Generated by Django 4.2.4 on 2023-08-24 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('firm', models.CharField(max_length=50, verbose_name='Raison Sociale')),
                ('first_name', models.CharField(max_length=50, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=50, verbose_name='Nom')),
                ('email', models.CharField(max_length=100, verbose_name='Email')),
                ('phone', models.CharField(max_length=15, verbose_name='Téléphone')),
                ('address', models.CharField(max_length=100, verbose_name='Adresse')),
                ('zipcode', models.CharField(blank=True, max_length=20, null=True, verbose_name='BP')),
                ('city', models.CharField(max_length=50, verbose_name='Ville')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Pays')),
                ('converted_to_client', models.BooleanField(default=False, verbose_name='Convertir en client')),
                ('converted_date', models.DateTimeField(blank=True, null=True, verbose_name='Date_conversion_en_client')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL, verbose_name='Créé par')),
            ],
        ),
    ]
