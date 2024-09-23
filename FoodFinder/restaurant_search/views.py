# foodfinder/restaurant_search/views.py

from django.shortcuts import render
import requests
import geocoder
from .forms import RestaurantSearchForm

GOOGLE_API_KEY = "***REMOVED***"


def get_restaurants(cuisine, min_rating, max_distance, user_location):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{user_location[0]},{user_location[1]}",
        "radius": max_distance * 1000,  # Convert km to meters
        "keyword": cuisine,
        "minprice": 0,  # minimum price level (0 = free, 4 = expensive)
        "maxprice": 4,  # maximum price level
        "opennow": True,  # Only show currently open restaurants
        "type": "restaurant",
        "key": GOOGLE_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("results", [])
        filtered_restaurants = [
            {
                "name": restaurant["name"],
                "rating": restaurant.get("rating"),
                "address": restaurant.get("vicinity"),
                "distance": restaurant.get("distance"),
            }
            for restaurant in data
            if restaurant.get("rating", 0) >= min_rating
        ]
        return filtered_restaurants
    return "Error fetching data from Google Places API"


def restaurant_search_view(request):
    form = RestaurantSearchForm()
    if request.method == "POST":
        form = RestaurantSearchForm(request.POST)
        if form.is_valid():
            cuisine = form.cleaned_data["cuisine"]
            min_rating = form.cleaned_data["min_rating"]
            max_distance = form.cleaned_data["max_distance"]
            g = geocoder.ip('me')
            if g.ok and g.latlng:
                latitude, longitude = g.latlng
                print(f"Latitude: {latitude}, Longitude: {longitude}")
            else:
                print("Could not retrieve location. Please check your network or IP service.")
            user_location = (latitude, longitude)

            restaurants = get_restaurants(cuisine, min_rating, max_distance, user_location)
            if isinstance(restaurants, str):
                return render(request, 'tempo/error.html', {'error': restaurants})
            return render(request, 'tempo/results.html', {'restaurants': restaurants})
    return render(request, 'tempo/search_form.html', {'form': form})
