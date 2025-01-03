import requests
import json
import os

# Replace with your actual API key
API_KEY = "AIzaSyBh9riyfFOAf-LLQql4gjWY3kuvjvLXaz8"
if API_KEY is None:
    raise ValueError("GOOGLE_MAPS_API_KEY environment variable not set.")

def geocode_address(address):
    """Geocodes an address using the Google Maps Geocoding API."""
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": API_KEY}
    response = requests.get(geocoding_url, params=params)
    response.raise_for_status() #Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        raise ValueError(f"Geocoding failed: {data['status']}")


def get_route(origin_address, destination_address):
    """Gets a route using the Google Maps Routes API."""

    origin_lat, origin_lng = geocode_address(origin_address)
    destination_lat, destination_lng = geocode_address(destination_address)


    routes_url = "https://routes.googleapis.com/directions/v2:computeRoutes"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }
    payload = {
        "origin": {"location": {"latLng": {"latitude": origin_lat, "longitude": origin_lng}}},
        "destination": {"location": {"latLng": {"latitude": destination_lat, "longitude": destination_lng}}},
        "travelMode": "DRIVE",  # Or other travel modes
        "routingPreference": "TRAFFIC_AWARE", # Example preference.  See API docs for options
        # Add other optional parameters as needed (see API documentation)
        "languageCode":"en" # Example language code
    }

    response = requests.post(routes_url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    data = response.json()
    return data


# Example usage
origin = "Grabowa 2 Łaziska górne"
destination = "Katowice ul Michała Kałuzy 27a"

try:
    route_data = get_route(origin, destination)
    print(json.dumps(route_data, indent=2))  # Print formatted JSON response
except (requests.exceptions.RequestException, ValueError) as e:
    print(f"An error occurred: {e}")


