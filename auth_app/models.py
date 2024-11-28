from django.db import models
from django.utils import timezone

class Utilisateur(models.Model):
    email = models.EmailField(primary_key=True)  # Make email the primary key
    nom = models.CharField(max_length=50, default='Unknown')
    prenom = models.CharField(max_length=50, default='Unknown')
    telephone = models.CharField(max_length=15, default='Unknown')
    mot_de_passe = models.CharField(max_length=10000, default='Unknown')
    last_login = models.DateTimeField(default=timezone.now)
    salt = models.CharField(max_length=400, default='')

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Login(models.Model):
    email = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, to_field='email')
    login_time = models.DateTimeField(default=timezone.now)  # Timestamp of the login attempt
    failed_at = models.CharField(null=True, default="no")  # Timestamp of the failed attempt, if applicable

    def __str__(self):
        if self.failed_at:
            return f"Failed login for {self.email} at {self.failed_at}"
        return f"Successful login for {self.email} at {self.login_time}"
