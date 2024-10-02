
from django.contrib import admin  # Django admin module
from django.urls import path , include      # URL routing
from authentication.views import *  # Import views from the authentication app
from profilePage.views import *
from restaurant_search.views import *
from django.conf import settings   # Application settings
# Static files serving

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('login/', login_page, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('reset-password/', reset_password_page, name='reset_password_page'),
    #path('profile/', add_to_favorites, name='add_to_favorites'),

    path('profile/', include('profilePage.urls')),
    path('', include('restaurant_search.urls')),
]
