from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import InscriptionForm
from .models import Utilisateur , Login
from hashlib import sha512
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib








import os

def generate_salt():
    """Generate a random salt."""
    return os.urandom(16).hex()  # Increased salt length to 16 bytes

def hash_password(password, salt):
    """Hash the password with salt using sha512."""
    return sha512((password + salt).encode()).hexdigest()

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Get the form data
            nom = form.cleaned_data['nom']
            prenom = form.cleaned_data['prenom']
            email = form.cleaned_data['email']
            telephone = form.cleaned_data['telephone']
            mot_de_passe = form.cleaned_data['mot_de_passe']

            # Generate a salt for password hashing
            salt = generate_salt()

            # Hash the password using the salt
            mot_de_passe_hash = hash_password(mot_de_passe, salt)

            # Save the user to the database with the salt and hashed password
            user = Utilisateur(
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                mot_de_passe=mot_de_passe_hash,
                salt=salt  # Save the salt to the database
            )
            user.save()

            messages.success(request, "Inscription réussie! Vous pouvez maintenant vous connecter.")
            return redirect('connexion')  # Redirect to login page
    else:
        form = InscriptionForm()

    return render(request, 'inscription.html', {'form': form})

def connexion_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        
        try:
            # Retrieve user from the database
            user = Utilisateur.objects.get(email=email)
            # Hash the entered password with the user’s stored salt
            mot_de_passe_hash = hash_password(mot_de_passe, user.salt)
            
            # Check if the hashed password matches the stored password
            if mot_de_passe_hash == user.mot_de_passe:
                # Store all user information in session variables
                request.session['user_info'] = {
                    'nom': user.nom,
                    'prenom': user.prenom,
                    'email': user.email,
                    'telephone': user.telephone,
                    'last_login': str(timezone.now()),
                }
                
                # Record successful login
                Login.objects.create(
                    email=user,  # ForeignKey relationship with Utilisateur
                    login_time=timezone.now()
                )
                sender_email = "youneszergine@gmail.com"  # Replace with your sender email
                sender_password = "natsihbuiynwcxbg"  # Replace with your sender email password
                receiver_email = user.email
                subject = "Login Alert"
                text = f"""
                Hello {user.nom},
                You just logged in successfully at {timezone.now()} from IP address {request.META.get('REMOTE_ADDR')}.
                If this was not you, please secure your account immediately.
                Regards,
                Security Team
                """
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{text}")



                return redirect('acceuil')
            else:
                # Incorrect password
                messages.error(request, "Email ou mot de passe incorrect.")
                
                # Record failed login attempt
                Login.objects.create(
                    email=user,  # ForeignKey relationship with Utilisateur
                    login_time=timezone.now(),
                    failed_at="yes"  # Ensure this field is in the Login model
                )
                sender_email = "youneszergine@gmail.com"  # Replace with your sender email
                sender_password = "natsihbuiynwcxbg"  # Replace with your sender email password
                receiver_email = user.email
                subject = "Login Alert"
                text = f"""
                Hello {user.nom},
                There is how try to anter your account at {timezone.now()} from IP address {request.META.get('REMOTE_ADDR')}.
                If this was not you, please secure your account immediately.
                Regards,
                Security Team
                """
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, f"Subject: {subject}\n\n{text}")
                
        
        except Utilisateur.DoesNotExist:
            messages.error(request, "Email ou mot de passe incorrect.")
            
    return render(request, 'connexion.html')

def acceuil(request):
    # Check if user information is in the session
    if 'user_info' in request.session:
        user_info = request.session['user_info']
        login_data = Login.objects.filter(email=user_info['email'])

    else:
        user_info = None  # No user is logged in
        login_data = None

    return render(request, 'acceuil.html', {'user_info': user_info , 'login_data': login_data} )


def deconnexion(request):
    logout(request)
    return redirect('connexion')
