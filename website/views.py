from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def home(request):
    # Check to see if logging in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenue à PrestCRM!")
            return redirect('home')
        else:
            messages.error(request, "Il y a une erreur, veuillez réessayer svp.")
            return redirect('home')
    else:
        return render(request, 'website/home.html')
def logout_user(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté...")
    return redirect('home')

def register_user(request):
    return render(request, 'website/register.html')