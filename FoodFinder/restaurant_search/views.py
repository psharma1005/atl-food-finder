from django.shortcuts import render
import requests
import geocoder
from .forms import RestaurantSearchForm
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from profilePage.models import FavoriteRestaurant 
import json
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect

GOOGLE_API_KEY = "***REMOVED***"

def get_place_details(place_id):
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": GOOGLE_API_KEY,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json().get("result", {})
        return data.get("reviews", [])
    return []


def restaurant_reviews_view(request, place_id):
    reviews = get_place_details(place_id)
    if not reviews:
        return render(request, 'tempo/error.html', {'error': "No reviews found or error fetching reviews."})

    return render(request, 'tempo/reviews.html', {'reviews': reviews})

def get_distance_via_road(user_lat, user_lng, restaurant_lat, restaurant_lng):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": f"{user_lat},{user_lng}",
        "destinations": f"{restaurant_lat},{restaurant_lng}",
        "key": GOOGLE_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['rows'][0]['elements'][0]['status'] == 'OK':
            return data['rows'][0]['elements'][0]['distance']['text']
    return "N/A"


def get_restaurants(cuisine, min_rating, max_distance, user_location):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{user_location[0]},{user_location[1]}",
        "radius": max_distance * 1000,
        "keyword": cuisine,
        "minprice": 0,
        "maxprice": 4,
        "opennow": True,
        "type": "restaurant",
        "key": GOOGLE_API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("results", [])
        filtered_restaurants = []

        for restaurant in data:
            rating = restaurant.get("rating", 0)
            if rating >= min_rating:
                restaurant_location = restaurant["geometry"]["location"]
                restaurant_lat = restaurant_location["lat"]
                restaurant_lng = restaurant_location["lng"]

                distance = get_distance_via_road(user_location[0], user_location[1], restaurant_lat, restaurant_lng)

                filtered_restaurants.append({
                    "name": restaurant["name"],
                    "rating": rating,
                    "address": restaurant.get("vicinity"),
                    "distance": distance,
                    "latitude": restaurant_lat,
                    "longitude": restaurant_lng,
                    "place_id": restaurant["place_id"],
                })

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
                latitude = g.latlng[0]
                longitude = g.latlng[1]
                user_location = (latitude, longitude)
            else:
                print("Could not retrieve location. Please check your network or IP service.")
                return render(request, 'tempo/error.html', {'error': "Could not retrieve user location."})

            restaurants = get_restaurants(cuisine, min_rating, max_distance, user_location)
            if isinstance(restaurants, str):
                return render(request, 'tempo/error.html', {'error': restaurants})

            restaurant_json = json.dumps(restaurants)
            return render(request, 'tempo/results.html', {'restaurant_json':restaurant_json,'restaurants': restaurants })

    return render(request, 'tempo/search_form.html', {'form': form})


def add_to_favorites(request):
    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        # Add logic to handle adding the restaurant to the favorites list
        # For example, saving to a database, etc.
        name = request.POST.get("name")
        address = request.POST.get("address")
        rating = request.POST.get("rating")
        FavoriteRestaurant.objects.create(
                    user=request.user,  
                    name=name,
                    rating=rating,
                    address=address,
        )
        print(rating)
        # Return a success response

        return redirect('/profile')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
