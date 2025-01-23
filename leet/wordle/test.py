import os
import requests
from geopy.geocoders import Nominatim
def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    if location:
        print("fail")
        return location.latitude, location.longitude
    else:
        return None
def distance_ors(origin_coords, destination_coords):
    # Initialize ORS API key
    api_key = "5b3ce3597851110001cf6248f4957c17e030403eb672c7f5b55dd3d8"
    if not api_key:
        raise ValueError("ORS_API_KEY environment variable not set.")

    # Initialize ORS client URL
    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car"

    

    # Prepare request
    headers = {'Authorization': api_key}
    params = {
        'start': f"{origin_coords[1]},{origin_coords[0]}",
        'end': f"{destination_coords[1]},{destination_coords[0]}"
    }

    # Call ORS API
    response = requests.get(ors_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        distance_km = data['features'][0]['properties']['summary']['distance'] / 1000
        duration_min = data['features'][0]['properties']['summary']['duration'] / 60
        return {
            "distance": round(distance_km, 1),
            "duration": round(duration_min,1)
        }
    else:
        raise ValueError(f"Error from ORS API: {response.status_code} - {response.text}")
distance_ors((50, 18),(51,18 ))
{'start': '50.19056255, 19.002081848586148', 'end': '51.3162851, 18.9429037'}
{'start': '50.19056255, 19.002081848586148', 'end': '51.5930209,18.9619491'}