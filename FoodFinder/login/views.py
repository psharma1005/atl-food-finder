from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic

from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

# Create your views here.


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("SOMEWHERE ELSE HANDLE THIS LATER")

    else:
        form = LoginForm()
    return render(request, 'login/login_2.html')
