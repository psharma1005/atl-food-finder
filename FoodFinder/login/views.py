from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic

# Create your views here.


def login(request):
    template = loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context, request))


class LoginView(generic.ListView):
    template_name = "polls/login.html"

    def get_queryset(self):
        return
