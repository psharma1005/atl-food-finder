from django.shortcuts import render
from .google_places import search_restaurants, sort_by_road_distance


def restaurant_search_view(request):
    user_location = (37.7749, -122.4194)
    query = request.GET.get('query', 'sushi')
    min_rating = request.GET.get('min_rating', 4.0)

    restaurants = search_restaurants(query, user_location, min_rating=float(min_rating))

    if isinstance(restaurants, str):
        return render(request, 'restaurant_search/error.html', {'error': restaurants})
    else:
        sorted_restaurants = sort_by_road_distance(restaurants, user_location)
        return render(request, 'restaurant_search/results.html', {'restaurants': sorted_restaurants[:5]})