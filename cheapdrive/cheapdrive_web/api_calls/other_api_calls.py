from multiprocessing import Value
from geopy.geocoders import Nominatim
from api_calls.api_exceptions import AddressError
import os
import openrouteservice
import requests
from bs4 import BeautifulSoup
from .api_calculations import get_coordinates

from django.contrib.gis.geos import Point
from entry.models import Station, StationPrices


    
def distance_ors(origin_coords, destination_coords):
    # Initialize ORS API key
    api_key =os.environ.get("ORS_API_KEY")
    if not api_key:
        raise ValueError("ORS_API_KEY environment variable not set.")

    # Initialize ORS client URL
    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car"

    

    # Get coordinates for origin and destination
    
    # Prepare request
    headers = {'Authorization': api_key}
    params = {
        'start': f"{origin_coords[1]},{origin_coords[0]}",
        'end': f"{destination_coords[1]},{destination_coords[0]}"
    }
    print(params)
    # Call ORS API
    response = requests.get(ors_url, headers=headers, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        distance_km = data['features'][0]['properties']['summary']['distance'] / 1000
        duration_min = data['features'][0]['properties']['summary']['duration'] / 60
        return (round(distance_km, 1),round(duration_min,1))
        
    else:
        raise ValueError(f"Error from ORS API: {response.status_code} - {response.text}")
    

import requests

def retrieve_stations_overpass( brand_names, limit=50000):
   
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Overpass QL query with LIMIT
    query = f"""
    [out:json];
    node
      ["amenity"="fuel"]
      (around:{360000},{51.5},{19.8});
    out {limit};
    """
    
    response = requests.post(overpass_url, data={'data': query})
    stations = []
    print(stations)
    if response.status_code == 200:
        data = response.json()
        if data['elements']:
            for station in data['elements']:
                tags = station.get('tags', {})
                station_name = tags.get('brand', '').lower()
                print(station)
                # Check if the brand name is in the provided list
                brand_name=station_name
                for brand in brand_names:
                    if brand.lower() in  station_name:
                        brand_name=brand.lower()
                        lat = station['lon']
                        lon = station['lat']
                    
                        # Append the station info as a dictionary to the stations list
                        stations.append({
                            'lat': lat,
                            'lon': lon,
                            'brand_name': brand_name,
                        })
                        print({
                            'lat': lat,
                            'lon': lon,
                            'brand_name': brand_name,
                        })
                        break
        
    else:
        raise ValueError("Overpass API request was unsuccessful")
    
    return stations

           

def scrape_prices(brand_name):
        url="https://www.autocentrum.pl/stacje-paliw/"+brand_name
       
        response = requests.get(url)
        #Initialize BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        diesel_price=0; lpg_price=0; pb95_price=0; pb98_price=0
        # Find all station items
        for fuel in soup.find_all('div', class_='last-prices-wrapper'):
            fuel_type = fuel.find('div', class_='fuel-logo').text.strip()
           
            if fuel_type=="pb" :
                price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
                pb95_price=price_element
            elif fuel_type=="pb+":
                price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
                pb98_price=price_element
            elif fuel_type=="on" or fuel_type=="on+":
                if fuel_type=="on+" and diesel_price!=0:#not taking on+ price if on price is available
                    pass
                else:
                    price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
                    diesel_price=price_element
            elif fuel_type=="lpg" or fuel_type=="lpg+" :
                if fuel_type=="lpg+" and lpg_price!=0:#not taking lpg+ price if lpg price is available
                    pass
                else:
                    price_element = fuel.find('div', class_='price-wrapper').text.split()[0]
                    lpg_price=price_element
        
        return(pb95_price,pb98_price,diesel_price,lpg_price)
