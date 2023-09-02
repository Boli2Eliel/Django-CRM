from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from authentication.models import Account
from userprofile.models import Profile

INPUT_CLASS = " w-full py-2 px-6 rounded-xl"
class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','email','password1', 'password2',)



class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Pseudo", "class": "form-control fw-semibold"}), label="Pseudo")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Email", "class": "form-control fw-semibold"}), label="Téléphone")
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Prénom", "class": "form-control fw-semibold"}), label="Prénom")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Nom", "class": "form-control fw-semibold"}), label="Nom")

    class Meta:
        model = Account
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_superuser']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-group'}),

        }

class UserUpdateSuiteForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Pseudo", "class": "form-control fw-semibold"}), label="Pseudo")

    class Meta:
        model = Account
        fields = ['username', 'email', 'is_staff', 'is_admin', 'is_superuser']
        exclude = ('first_name', 'last_name', )
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-group'}),

        }
class ProfileUpdateForm(forms.ModelForm):
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Adresse", "class": "form-control fw-semibold"}), label="Adresse")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Téléphone", "class": "form-control fw-semibold"}), label="Téléphone")
    job_function = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Profession", "class": "form-control fw-semibold"}), label="Profession")

    class Meta:
        model = Profile
        fields = ['address', 'phone', 'job_function', 'profile_image']
