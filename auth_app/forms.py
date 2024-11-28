from django import forms
from django.contrib.auth.hashers import make_password
from .models import Utilisateur

class InscriptionForm(forms.Form):
    nom = forms.CharField(max_length=50, label="Nom")
    prenom = forms.CharField(max_length=50, label="Prénom")
    email = forms.EmailField(max_length=100, label="Email")
    telephone = forms.CharField(max_length=20, label="Numéro de téléphone")
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    confirm_mot_de_passe = forms.CharField(widget=forms.PasswordInput, label="Confirmer le mot de passe")

    def clean(self):
        cleaned_data = super().clean()
        mot_de_passe = cleaned_data.get('mot_de_passe')
        confirm_mot_de_passe = cleaned_data.get('confirm_mot_de_passe')

        if mot_de_passe != confirm_mot_de_passe:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        if len(mot_de_passe) < 8:
            raise forms.ValidationError("Le mot de passe doit comporter au moins 8 caractères.")
        return cleaned_data
