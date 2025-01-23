from api_calls.other_api_calls import scrape_prices,retrieve_stations_overpass
from .models import StationPrices,Station
from django.contrib.gis.geos import Point

def update_brand_prices():
    brands = ["circle-k-statoil","orlen","shell","amic","lotos","lotos-optima","bp","moya", "auchan", "tesco", "carrefour","olkop","leclerc","intermarche","pieprzyk","huzar","total"]
    for brand_name in brands:
        pb95_price, pb98_price, diesel_price, lpg_price = scrape_prices(brand_name)
        
        # Handle brand name variations
        if brand_name == 'circle-k-statoil':
            brand_name = 'circle k'
        elif brand_name == 'lotos-optima':
            brand_name = 'lotos optima'
        

        # Clean up prices - handle potential errors more robustly
        price_mapping = {
            'pb95_price': pb95_price,
            'pb98_price': pb98_price,
            'diesel_price': diesel_price,
            'lpg_price': lpg_price,
        }
        for key, value in price_mapping.items():
            price_mapping[key] = None if value == 0 or value is None else float(str(value).replace(",", "."))
        try:
            StationPrices.objects.update_or_create(
            brand_name=brand_name,
            defaults={
                'pb95_price': price_mapping['pb95_price'],
                'pb98_price': price_mapping['pb98_price'],
                'diesel_price': price_mapping['diesel_price'],
                'lpg_price': price_mapping['lpg_price'],
            }
            )
        except:
            print(brand_name)
            
def update_station_objects():
    brand_names = ["circle k","orlen","shell","amic","lotos","lotos-optima","bp","moya", "auchan", "tesco", "carrefour","olkop","leclerc","intermarche","pieprzyk","huzar","total"]
    created_stations = []
    all_stations=retrieve_stations_overpass(brand_names)
    for station_data in all_stations:
        brand_name = station_data['brand_name']
        lat = station_data['lat']
        lon = station_data['lon']
    
        # GIS Point (longitude, latitude)
        location = Point(lat, lon)
        try:
            # Get the StationPrices object or raise an exception if not found
            station_prices = StationPrices.objects.get(brand_name=brand_name)
        
            # Create Station object
            station_obj, created = Station.objects.get_or_create(
            
            location=location,
            station_prices=station_prices
            )
            print(f"Added station: {brand_name} at {station_obj.location}")
            created_stations.append(station_obj)

        except StationPrices.DoesNotExist:
            print(f"StationPrices for brand '{brand_name}' not found. Skipping station.")
        
    
    return created_stations    