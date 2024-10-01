from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
import re




# Create your views here.


def home(request):
    return render(request, "home.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username')
            return redirect('/login/')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/login')

def has_valid_email_ending(string):
    valid_endings = (".com", ".net", ".org", ".edu", ".gov", ".io")
    return string.endswith(valid_endings)

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if len(first_name) < 3 or len(last_name) < 3:
            messages.info(request, "First and Last name must be longer than 2 characters!")
            return redirect('/register/')

        if not has_valid_email_ending(email):
            messages.info(request, "Please enter a proper email!")
            return redirect('/register/')

        if len(username) < 4 or len(password) < 4:
            messages.info(request, "Username and Password must be longer than 4 characters!")
            return redirect('/register/') 
        
        user = User.objects.filter(email=email)
        user_ = User.objects.filter(username=username)
        if user.exists() or user_.exists():
            messages.info(request, "Account already exists!")
            return redirect('/register/')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )

        user.set_password(password)
        user.save()


        user.profile.favorite_cusine = "Indian"
        user.profile.save()


        messages.info(request, "Account Created.")
        return redirect('/login/')

    return render(request, 'register.html')


def reset_password_page(request):
    if request.method == "POST":

        email = request.POST.get("email")
        user = User.objects.filter(email=email)

        if not user:

            messages.error(request, "Email not found!")
            return redirect('/reset-password/')

    return render(request, "reset_password.html")
