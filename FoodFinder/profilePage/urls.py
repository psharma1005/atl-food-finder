from django.urls import path
from .views import *

app_name = 'profilePage'  # This correctly defines the namespace

urlpatterns = [
    path('', profile_page, name='profile_page'),  # Assumes profile_page view is imported
]