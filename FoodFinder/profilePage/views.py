from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import Profile  # Import the Profile model
from profilePage.models import FavoriteRestaurant  # Import FavoriteRestaurant model

from functools import wraps
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control

def no_cache(view_func):
    @wraps(view_func)
    @never_cache
    @cache_control(no_store=True, must_revalidate=True, no_cache=True)
    def wrapped_view(*args, **kwargs):
        response = view_func(*args, **kwargs)
        return response
    return wrapped_view

@login_required
@no_cache
def profile_page(request):
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name
    
    profile = Profile.objects.get(user=request.user)
    favorite_restaurants = FavoriteRestaurant.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'favorite_cusine' in request.POST:
            # Update favorite cuisine
            favorite_cusine = request.POST.get('favorite_cusine')
            profile.favorite_cusine = favorite_cusine
            profile.save()
        
        if 'restaurant_name' in request.POST:
            # Update favorite restaurant
            restaurant_name = request.POST.get('restaurant_name')
            restaurant_rating = request.POST.get('restaurant_rating')
            restaurant_address = request.POST.get('restaurant_address')
            restaurant_distance = request.POST.get('restaurant_distance')

            # Create and save a new favorite restaurant entry
            if restaurant_name and restaurant_rating and restaurant_address and restaurant_distance:
                FavoriteRestaurant.objects.create(
                    user=request.user,
                    name=restaurant_name,
                    rating=restaurant_rating,
                    address=restaurant_address,
                    distance=restaurant_distance
                )
        
        return redirect('profile')  # Redirect to avoid resubmission on reload

    context = {
        "greeting": f"Hello {username}",
        "first_name": first_name,
        "last_name": last_name,
        "favorite_cusine": profile.favorite_cusine,
        "favorite_restaurants": favorite_restaurants  # Pass the restaurants to the template
    }

    return render(request, 'profile.html', context)
