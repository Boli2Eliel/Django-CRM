# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Les utilisateurs doivent avoir une adresse mail.")
        if not username:
            raise ValueError("Les utilisateurs doivent avoir un pseudo.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def get_profile_image_filepath(self, filename):
    return f'profile_images/{str(self.pk)}/{"profile_image.png"}'

def get_default_profile_image():
    return 'img/avatar.jpg'

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="Adresse mail", max_length=120, unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    job_function = models.CharField(max_length=200, null=True)
    date_joined = models.DateTimeField(verbose_name="Date d'enregistrement", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Dernière connexion", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email = models.BooleanField(default=True)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username
    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]
    def has_perm(self,perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

# Attention : il faudra ensuite ajouter cette ligne dans settings.py """ AUTH_USER_MODEL = 'authentication.Account' """