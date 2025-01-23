from queue import Full
import time
from concurrent.futures import ThreadPoolExecutor
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point
from django.db.models import Q
from api_calls.api_calculations import get_coordinates
import math
from entry.models import Station

def calculate_perpendicular_distance(lat1, lon1, lat2, lon2, lat3, lon3):
    start_time = time.time()
    lat1, lon1, lat2, lon2, lat3, lon3 = map(math.radians, [lat1, lon1, lat2, lon2, lat3, lon3])
    dx12 = lon2 - lon1
    dy12 = lat2 - lat1
    dx13 = lon3 - lon1
    dy13 = lat3 - lat1
    cross_product = abs(dx12 * dy13 - dy12 * dx13)
    denominator = math.sqrt(dx12**2 + dy12**2)
    result = (cross_product / denominator) * 6371
    return result

def calculate_distance(lat1, lon1, lat2, lon2):
    start_time = time.time()
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    result = 6371.0 * c
    return result

def find_gas_within_range(origin, destination, estimated_range, full_tank_range):
    start_time = time.time()
    origin_lat, origin_lon = origin
    dest_lat, dest_lon = destination
    stations_within_route = []
    origin_point = Point(origin_lon, origin_lat)
    destination_point = Point(dest_lon, dest_lat)
    
    stations_within_range = Station.objects.filter(
        location__distance_lte=(origin_point, D(km=0.7 * estimated_range))
    )
    
    stations_that_will_be_enough = stations_within_range.filter(
        location__distance_lte=(destination_point, D(km=0.7 * full_tank_range))
    )
    if not stations_that_will_be_enough:
       with ThreadPoolExecutor() as executor:
            station_distances = executor.map(
            lambda station: calculate_distance(dest_lat, dest_lon, station.location.y,station.location.x), 
            stations_within_range
            )
       # Sort stations by distance
       closest_station = min(zip(stations_within_range, station_distances), key=lambda x: x[1])[0]
       print(closest_station)
       return ("failure",closest_station)
    print(f"Finding stations within range took {time.time() - start_time:.6f} seconds")
    return stations_that_will_be_enough

def find_gas_near_route(stations,origin,destination):
    start_time = time.time()
    origin_lat, origin_lon = origin
    dest_lat, dest_lon = destination
    detour_radius_km=max(calculate_distance(origin_lat,origin_lon,dest_lat,dest_lon)/4,10)  
    stations_within_route=[]
    for station in stations:
        distance = calculate_perpendicular_distance(origin_lat, origin_lon, dest_lat, dest_lon, station.location.y, station.location.x)
        if distance <= detour_radius_km:
            stations_within_route.append(station)
            print(str(station.id)+", ")
    
    print(f"Finding stations near route took {time.time() - start_time:.6f} seconds")
    return stations_within_route

def find_best_gas_stations(origin, destination, estimated_range, full_tank_range,stations_along=None, top_n=3):
    total_start_time = time.time()

    if not origin or not destination:
        return []

    start_within_range_time = time.time()
    stations_within_range = find_gas_within_range(origin, destination, estimated_range, full_tank_range)
    if stations_within_range[0]=="failure":
        print("FAIL")
        if not stations_along:
            stations_along=[]
        closest_station_along=stations_within_range[1]
        print(closest_station_along.location.y,closest_station_along.location.x)
        stations_along.append(stations_within_range[1])
        print(closest_station_along.location)
        return find_best_gas_stations((closest_station_along.location.y,closest_station_along.location.x),destination,full_tank_range,full_tank_range,stations_along)
        
    stations_near_route=find_gas_near_route(stations_within_range,origin,destination)
        
    print(f"Finding stations near route and some other things took {time.time() - start_within_range_time:.6f} seconds")
    print(destination)
   
    station_by_distances = []

    def compute_total_distance(station):
        start_compute_time = time.time()
        distance_origin_to_station = calculate_distance(origin[0], origin[1], station.location.y, station.location.x)
        distance_station_to_destination = calculate_distance(station.location.y, station.location.x, destination[0], destination[1])
        result = (station, distance_origin_to_station + distance_station_to_destination)
       
        print(f"Computing total distance for a station took {time.time() - start_compute_time:.6f} seconds")
        return result

    start_parallel_time = time.time()
    with ThreadPoolExecutor() as executor:
        results = executor.map(compute_total_distance, stations_near_route)
        
        station_by_distances = sorted(results, key=lambda x: x[1])
    print(f"Parallel computation took {time.time() - start_parallel_time:.6f} seconds")

    print(f"Total execution time: {time.time() - total_start_time:.6f} seconds")
    print(station_by_distances[-1][0].location.y,station_by_distances[-1][0].location.x)
    print("wefwef")
    print(stations_along)
    if stations_along:
        return [[i for i in stations_along] + [station] for station, _ in station_by_distances[:top_n]]
    else:
            return [[station] for station,_  in station_by_distances[:top_n]]
