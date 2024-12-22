
import googlemaps 
import os
from .api_exceptions import AddressError

def address_validation_and_distance(start,finish):
    api_key = os.environ.get("GOOGLE_API_KEY")  # Get from environment variable
  
    if api_key is None:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    gmaps = googlemaps.Client(key=api_key)
    element = gmaps.distance_matrix(
        origins=start,
        destinations=finish,
        mode="driving",
        )
   # element={'destination_addresses': ['Zlota 59, 00-120 Warszawa, Poland'], 'origin_addresses': ['Kaluzy 27a, 40-750 Katowice, Poland'], 
            # 'rows': [{'elements': [{'distance': {'text': '313 km', 'value': 313428}, 'duration': {'text': '3 hours 12 mins', 'value': 11506}, 'status': 'OK'}]}], 'status': 'OK'} 
                                                                                                               
    if element['rows'][0]['elements'][0]["status"] == 'OK':
        distance = float(element['rows'][0]['elements'][0]['distance']['value'])/1000
        duration = float(element['rows'][0]['elements'][0]['duration']['value'])/60
        return distance,duration
    
    if element["origin_addresses"][0]=='':
        raise AddressError("origin")
    
    if element["destination_addresses"][0]=='':
        raise AddressError("destination")
    

  # If both addresses are wrong (unlikely but possible)
    raise AddressError("both addresses")
    
