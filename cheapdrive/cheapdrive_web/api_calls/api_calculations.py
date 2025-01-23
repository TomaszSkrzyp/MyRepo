from geopy.distance import geodesic

from geopy.geocoders import Nominatim

def calculate_gas_coords(origin,destination,drive_range, distance, iteration):
    ratio=drive_range/distance*((15-2*iteration)/16)
    delta_lat=destination[1]-origin[1]
    delta_lon=destination[0]-origin[0]
    return origin[0]+ratio*delta_lat,origin[1]+ratio*delta_lon

def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None
    
    
    
    