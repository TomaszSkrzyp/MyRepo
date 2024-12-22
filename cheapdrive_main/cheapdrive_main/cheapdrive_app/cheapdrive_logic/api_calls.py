import os
import googlemaps

from exceptions import AddressError

def route_to_distance(start,finish):
    #api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    #gmaps = googlemaps.Client(key=api_key)
   
    #Calculate the route matrix
    #response = gmaps.distance_matrix(
        #origins=start,
       # destinations=finish,
       # mode="driving")
    #print(response)
    element={'destination_addresses': ['Zlota 59, 00-120 Warszawa, Poland'], 'origin_addresses': ['Kaluzy 27a, 40-750 Katowice, Poland'], 
             'rows': [{'elements': [{'distance': {'text': '313 km', 'value': 313428}, 'duration': {'text': '3 hours 12 mins', 'value': 11506}, 'status': 'OK'}]}], 'status': 'OK'} 
                                                                                                                  
    if element['rows'][0]['elements'][0]["status"] == 'OK':
        distance = float(element['rows'][0]['elements'][0]['distance']['value'])/1000
        duration = float(element['rows'][0]['elements'][0]['duration']['value'])/60
        return distance
    
    if element["origin_addresses"][0]=='':
        raise AddressError("origin")

    if element["destination_addresses"][0]=='':
        raise AddressError("destination")
    

  # If both addresses are wrong (unlikely but possible)
    raise AddressError("both addresses")
