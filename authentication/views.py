# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from userprofile.forms import UserUpdateForm, UserUpdateSuiteForm
from .forms import LoginForm, SignUpForm
from .models import Account


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Bienvenue à PrestCRM App!")
                return redirect("dashboard")
            else:
                msg = 'Informations erronées! Merci de vérifier et réessayer.'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'Utilisateur créé avec succès!'
            success = True
            return redirect("dashboard")
        else:
            msg = 'Formulaire non valide'
        return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})

def users_list(request):
    accounts = Account.objects.all()
    return render(request, "accounts/accounts_list.html", {"accounts": accounts})

@login_required()  # "LOGIN_URL = 'user-login'" # for decorators a été ajouté dans le settings
def user_update(request,pk):
    current_user = Account.objects.get(id=pk)
    if request.method == 'POST':
        user_form = UserUpdateSuiteForm(request.POST or None, instance=current_user)
        if user_form.is_valid :
            # if profile_form.is_valid:
            user_form.save()
            return redirect('accounts')
    else:
        user_form = UserUpdateSuiteForm(instance=current_user)

    context = {
        'user_form': user_form,
    }
    return render(request, 'accounts/account_update.html', context)
