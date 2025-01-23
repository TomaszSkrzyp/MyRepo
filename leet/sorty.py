from geopy.geocoders import Nominatim

import requests

def find_gas_stations(lat, lon, radius=10000, limit=10):
    # Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Overpass QL query with LIMIT
    query = f"""
    [out:json];
    node
      ["amenity"="fuel"]
      (around:{radius},{lat},{lon});
    out {limit};
    """
    brand_names = ["circle k","orlen","shell","amic","lotos","lotos optima","bp","moya", "auchan", "tesco", "carrefour","olkop","leclerc","intermarché","pieprzyk","huzar","total"]

    # Send the request
    response = requests.post(overpass_url, data={'data': query})

    # Check if the request was successful
    stations_count=0
    if response.status_code == 200:
        data = response.json()
        if data['elements']:
            for station in data['elements']:
                name = station.get('tags', {}).get('name', 'Unnamed Gas Station')
                lat = station['lat']
                lon = station['lon']
                
                 
                if any(brand.lower() in name.lower() for brand in brand_names):
                        pass
                else:
                    print(f"Name: {name}\n")
        else:
            print("No gas stations found in this area.")
    else:
        print(f"Error: {response.status_code}")

# Example usage for New York City coordinates

def geocode_address(address):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude) if location else None


origin = geocode_address("Warszawa")
destination=geocode_address("Kaluzy katowice poland")
total_distance = 320
num_stops = 1

x=find_gas_stations(origin[0],origin[1])
print(x)