
import googlemaps 
import os
from .api_exceptions import AddressError
import requests

def address_validation_and_distance(origin,destination):
    api_key = os.environ.get("GOOGLE_API_KEY")  # Get from environment variable
  
    if api_key is None:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    gmaps = googlemaps.Client(key=api_key)
    element = gmaps.distance_matrix( origins=origin,destinations=destination,mode="driving", )
    #element={'destination_addresses': ['Gdansk poland'], 'origin_addresses': ['Kaluzy 27a, 40-750 Katowice, Poland'], 
             #'rows': [{'elements': [{'distance': {'text': '548 km', 'value': 548428}, 'duration': {'text': '5 hours 12 mins', 'value': 11506}, 'status': 'OK'}]}], 'status': 'OK'} 
    origin,destination=element["origin_addresses"][0],element["destination_addresses"][0]  
  
    if element['rows'][0]['elements'][0]["status"] == 'OK':
        distance = float(element['rows'][0]['elements'][0]['distance']['value'])/1000
        duration = float(element['rows'][0]['elements'][0]['duration']['value'])/60
        return distance,duration,origin,destination
    
    if origin=='' and destination=='':
        raise AddressError("both addresses")
    if origin=='':
        raise AddressError("origin address")
    
    if destination=='':
        raise AddressError("destination address")
    
    if element['rows'][0]['elements'][0]["status"] == 'ZERO_RESULTS':
        raise AddressError("addresses. No valid way between origin and destination")
    
def distance_gmaps(origin,destination): #A paid alternative to other_api_calls.py/distance_ors. doesnt validate addresses
    api_key = os.environ.get("GOOGLE_API_KEY")  
  
    if api_key is None:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    gmaps = googlemaps.Client(key=api_key)
    element = gmaps.distance_matrix(origins=origin,destinations=destination,mode="driving", )
    #element=""{'destination_addresses': ['Gdansk, Poland'], 'origin_addresses': ['Warszawska 10, 63-640 Chojêcin, Poland'], 'rows': [{'elements': [{'distance': {'text': '2,030 km', 'value': 2030325}, 'duration': {'text': '1 day 12 hours', 'value': 128346}, 'status': 'OK'}]}], 'status': 'OK'}
    if element['rows'][0]['elements'][0]["status"] == 'OK':
        distance = float(element['rows'][0]['elements'][0]['distance']['value'])/1000
        duration = float(element['rows'][0]['elements'][0]['duration']['value'])/60
        return distance,duration
    if origin=='' and destination=='':
        raise AddressError("one of the addresses")
    
    if element['rows'][0]['elements'][0]["status"] == 'ZERO_RESULTS':
        raise AddressError("addresses. No valid way between origin and destination")
    
    
def get_route_distance(origin, destination):
    """
    Returns the distance of the route from origin to destination using an API (e.g., Google Maps).
    """
    api_key = os.environ.get("GOOGLE_API_KEY")  
    route_url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    response = requests.get(route_url)
    
    if response.status_code == 200:
        directions_data = response.json()
        if directions_data['status'] == 'OK':
            legs = directions_data['routes'][0]['legs'][0]
            return legs['distance']['value'] / 1000, legs['steps']  # In kilometers
    return None, None  


