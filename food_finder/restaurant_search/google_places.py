import requests

API_KEY = '***REMOVED***'


def search_restaurants(query, location, radius=5000, type="restaurant", min_rating=None):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": API_KEY,
        "location": f"{location[0]},{location[1]}",
        "radius": radius,
        "keyword": query,
        "type": type,
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] != 'OK':
        return f"Error: {data['status']}"

    restaurants = data.get('results', [])
    if min_rating:
        restaurants = [restaurant for restaurant in restaurants if restaurant.get('rating', 0) >= min_rating]

    return restaurants


def get_distance_by_road(user_location, restaurant_location):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": f"{user_location[0]},{user_location[1]}",
        "destinations": f"{restaurant_location[0]},{restaurant_location[1]}",
        "key": API_KEY,
        "mode": "driving"
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        distance = data['rows'][0]['elements'][0]['distance']['value']
        return distance
    else:
        return float('inf')


def sort_by_road_distance(restaurants, user_location):
    distances = []
    for restaurant in restaurants:
        restaurant_location = (
            restaurant['geometry']['location']['lat'],
            restaurant['geometry']['location']['lng']
        )
        distance = get_distance_by_road(user_location, restaurant_location)
        distances.append((restaurant, distance))

    sorted_restaurants = sorted(distances, key=lambda x: x[1])
    return sorted_restaurants


