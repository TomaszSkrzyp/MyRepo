
import math
from geopy.distance import geodesic

from api_calls.api_calculations import get_coordinates
from api_calls.google_api_calls import distance_gmaps
from api_calls.other_api_calls import distance_ors

from concurrent.futures import ThreadPoolExecutor

def local_distance_fallback(coord1, coord2):
    return geodesic(coord1, coord2).km*1.2

def parallel_distance_calculations(orig_dest_pairs):
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda pair: get_ptp_distance(*pair), orig_dest_pairs)
    return list(results)

def get_ptp_distance(origin,destination, origin_coords,destination_coords):
    if geodesic(origin_coords, destination_coords).km < 50:
        
        print("Using Haversine")
        return local_distance_fallback(origin_coords, destination_coords), 0  # Approximate no traffi
    try:
        
        print("Using ORS API")
        return distance_ors(origin_coords,destination_coords)
    except ValueError:
       
        print("Using Google Maps API")
        return distance_gmaps(origin or origin_coords, destination or destination_coords)
    
import time    
def determinate_best_route(origin,routes,destination,price_of_fuel):
    def compute_route_params(origin, stations, destination):
        for i in stations:
            print(str(i.id)+", ")
        duration_list=[]
        origin_coords = get_coordinates(origin)
        destination_coords = get_coordinates(destination)
        #Prepare station coordinates list for parallel processing
        station_coords = [(stations[i].location.y, stations[i].location.x) for i in range(len(stations))]
        
        
        # Calculate all distances in parallel
       
        route_pairs = [
        (origin, None, origin_coords, station_coords[0])
        ] + [
        (None, None, station_coords[i], station_coords[i + 1]) for i in range(len(stations) - 1)
        ] + [
        (None, destination, station_coords[-1], destination_coords)
        ]       
        route_params = parallel_distance_calculations(route_pairs)

        
        return route_params
    
    best_route_distance = None
    best_route_duration = None
    best_distance = float('inf')  # Use infinity for better clarity
    best_duration = float('inf')

    results = []  # Store detailed results for each route

    for i, route in enumerate(routes):
        start = time.time()
        
        # Compute distances and durations for the current route
        route_params = compute_route_params(origin, route, destination)
        distances, durations = zip(*route_params)

        # Store results for reporting
        route_data = {
            'route': i,
            'distances': list(distances),
            'durations': list(durations),
        }
        results.append(route_data)

        # Check for the best distance
        total_distance = sum(distances)
        if total_distance < best_distance:
            best_distance = total_distance
            best_route_distance = route_data

        # Check for the best duration
        total_duration = sum(durations)
        if total_duration < best_duration:
            best_duration = total_duration
            best_route_duration = route_data

        print(f"Time for processing route {i}: {time.time() - start:.2f} seconds")

    return ( best_route_duration,best_route_distance
    )

    