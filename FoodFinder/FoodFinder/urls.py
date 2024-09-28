
from django.contrib import admin  # Django admin module
from django.urls import path       # URL routing
from authentication.views import *  # Import views from the authentication app
from profilePage.views import *
from restaurant_search.views import *
from django.conf import settings   # Application settings
# Static files serving

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('accounts/login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('reset-password/', reset_password_page, name='reset_password_page'),
    path('profile/', profile_page, name='profile'),
    path('search/', restaurant_search_view, name='search')
]
