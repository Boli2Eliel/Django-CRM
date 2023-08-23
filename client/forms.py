from django import forms
from .models import Client


class AddClientForm(forms.ModelForm):
    firm = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Raison Sociale (Si personne morale)", "class": "form-control fw-semibold"}), label="")
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Prénom", "class": "form-control fw-semibold"}), label="")
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Nom", "class": "form-control fw-semibold"}), label="")
    email = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Email", "class": "form-control fw-semibold"}), label="")
    phone = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Téléphone", "class": "form-control fw-semibold"}), label="")
    address = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Adresse", "class": "form-control fw-semibold"}), label="")
    city = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Ville", "class": "form-control fw-semibold"}), label="")
    zipcode = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "B.P", "class": "form-control fw-semibold"}), label="")

    # country = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Pays", "class":"form-control fw-semibold"}), label="")

    class Meta:
        model = Client
        exclude = ("user", "created_by", "converted_date")


"""class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-group'}),
        }
class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)"""
