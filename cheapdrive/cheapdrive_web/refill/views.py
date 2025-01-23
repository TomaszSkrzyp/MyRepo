
from typing import final
from geopy import distance
from api_calls.api_exceptions import AddressError
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from .route_choice import determinate_best_route

from api_calls.api_calculations import get_coordinates
from api_calls.google_api_calls import distance_gmaps
from api_calls.other_api_calls import distance_ors

from .models import Vehicle_data, Trip
from .create_models import create_trip, create_vehicle
from .forms import LoadDataForm
import logging
from .gas_station_looker import find_best_gas_stations
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt




def validate_fuel_data(tank_size, cur_fuel, fuel_input_type, cur_fuel_percentage):
    """Validates fuel-related data."""
    if float(tank_size) <= 0:
        raise ValidationError("Tank size must be positive.")
    if float(cur_fuel) < 0:
        raise ValidationError("Current fuel cannot be negative.")
    if fuel_input_type == 'percentage':
        if not 0 <= cur_fuel_percentage <= 100:
            raise ValidationError("Fuel percentage must be between 0 and 100.")
 
logger = logging.getLogger(__name__)  # Get a logger instance

@csrf_exempt
def load_data(request):
    
    try:
        vehicle_id,trip_id=scrape_query_paramaters(request.GET)
    except KeyError as e:
          messages.error(request, f"Invalid query parameters: {e}")
          logger.exception("Invalid query parameters:")
    except TypeError as e:
          messages.error(request, f"An unexpected error occurred: {e}")
          logger.exception("Unexpected Error:")
    trip=None
    vehicle=None

    if trip_id:
        trip = get_object_or_404(Trip, id=trip_id)
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle_data, id=vehicle_id)

    if request.method == 'POST':
        form = LoadDataForm(request.POST)
        if form.is_valid():
            try:
                # Extract form data
                origin_address = form.cleaned_data['origin_address']
                destination_address = form.cleaned_data['destination_address']
                tank_size = form.cleaned_data['tank_size']
                fuel_type = form.cleaned_data['fuel_type']
                fuel_consumption_per_100km = form.cleaned_data['fuel_consumption_per_100km']
                price_of_fuel = form.cleaned_data['price_of_fuel']
                currency = form.cleaned_data['currency']
                fuel_input_type = 'liters' if form.cleaned_data['cur_fuel_liters_check'] else 'percentage'
                cur_fuel_percentage = form.cleaned_data['cur_fuel_percentage'] if fuel_input_type == 'percentage' else None
                cur_fuel = form.cleaned_data['cur_fuel'] if fuel_input_type == 'liters' else (cur_fuel_percentage / 100) * tank_size

                # Validate fuel data
                validate_fuel_data(tank_size, cur_fuel, fuel_input_type, cur_fuel_percentage)
                
                user = request.user if request.user.is_authenticated else None
                guest_id = request.session.session_key if request.user.is_authenticated else None
                



                vehicle_id = create_vehicle(tank_size, fuel_type, cur_fuel, fuel_consumption_per_100km, price_of_fuel, currency)    
                vehicle = Vehicle_data.objects.get(id=vehicle_id)  # Retrieve the created Vehicle object  
                if not vehicle_id:
                    
                    messages.error(request, "Vehicle creation failed")
                    
                    
                    return render(request, 'refill/load_data.html', {
                        'vehicle_id': vehicle.id if vehicle else None,
                        'trip_id': trip.id if trip else None,
                        'form': form,
                     })
                

                trip_id = create_trip(origin_address, destination_address,currency, user, guest_id,vehicle_id)
                trip = Trip.objects.get(id=trip_id)  # Retrieve the created Trip object
                if not trip_id:
                   
                    messages.error(request, "Trip creation failed")
                    
                    return render(request, 'refill/load_data.html', {
                        'vehicle_id': vehicle.id if vehicle else None,
                        'trip_id': trip.id if trip else None,
                        'form': form,
                    })
                
                print(trip.total_distance())
                    
                if request.user.is_authenticated:
                      vehicle.user = request.user
                      vehicle.save()
                request.session['allowed_to_access_refill_views'] = True
                if vehicle.need_refill(trip.total_distance()):
                    messages.error(request, "Need some juice")
                    return redirect(f"{reverse('refill:refill_management')}?vehicle_id={vehicle_id}&trip_id={trip_id}")
                return redirect(f"{reverse('refill:results')}?vehicle_id={vehicle_id}&trip_id={trip_id}")

            except ValidationError as e:
                messages.error(request, f"Validation Error: {e}")
                logger.exception("Validation Error:")
            except (KeyError, ValueError, AddressError) as e:
                messages.error(request, f"Invalid input: {e}. Check the spelling and try again")
                logger.exception("Invalid Input Error:")

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                logger.exception("Unexpected Error:")

        # Re-render form with errors and original data
        return render(request, 'refill/load_data.html', {
            'vehicle_id': vehicle.id if vehicle else None,
            'trip_id': trip.id if trip else None,
            'form': form,
        })

    else:
        # Render form pre-filled with existing trip or vehicle data if provided
        initial_data = {}
        if trip:
            initial_data.update({
                'origin_address': trip.origin_address,
                'destination_address': trip.destination_address,
            })
        if vehicle:
            initial_data.update({
                'tank_size': vehicle.tank_size,
                'fuel_type': vehicle.fuel_type,
                'fuel_consumption_per_100km': vehicle.fuel_consumption_per_100km,
            })

        form = LoadDataForm(initial=initial_data)
        return render(request, 'refill/load_data.html', {
            'vehicle_id': vehicle.id if vehicle else None,
            'trip_id': trip.id if trip else None,
            'form': form,
        })



def refill_management(request):
    if not request.session.get('allowed_to_access_refill_views', True):
        messages.error(request, "You are not authorized to access this page.")
        return redirect(reverse('entry:load_data'))
    
    request.session['allowed_to_access_refill_views'] = False

    # Extract and validate query parameters
    try:
        vehicle_id, trip_id = scrape_query_paramaters(request.GET)
    except (KeyError, TypeError) as e:
        messages.error(request, f"Invalid query parameters: {e}")
        logger.exception("Error in query parameters")
        request.session['allowed_to_access_refill_views'] = True
        return redirect(reverse('entry:load_data'))

    # Fetch trip and vehicle details
    trip = get_object_or_404(Trip, id=trip_id) if trip_id else None
    vehicle = get_object_or_404(Vehicle_data, id=vehicle_id) if vehicle_id else None

    if not trip or not vehicle:
        messages.error(request, "Trip or vehicle not found.")
        request.session['allowed_to_access_refill_views'] = True
        return redirect(reverse('entry:load_data'))

    # Estimate driving ranges
    est_drive_range =float( vehicle.cur_fuel / vehicle.fuel_consumption_per_100km * 100)
    full_tank_range = float(vehicle.tank_size / vehicle.fuel_consumption_per_100km * 100)

    # Get coordinates for trip origin and destination
    origin_coords = get_coordinates(trip.origin_address())
    destination_coords = get_coordinates(trip.destination_address())

    # Find best gas station routes
    best_station_routes = find_best_gas_stations(
        origin_coords, destination_coords, est_drive_range, full_tank_range
    )

    # Logging station details
    for route in best_station_routes:
        station_ids = ", ".join(str(station.id) for station in route)
        logger.info(f"Station IDs: {station_ids}")
        print(f"Station IDs: {station_ids}")

    # Determine best route (time vs. distance)
    best_route_by_time, best_route_by_distance = determinate_best_route(
        trip.origin_address(), best_station_routes, trip.destination_address(), vehicle.price_of_fuel
    )
    print(best_route_by_time,best_route_by_distance)
    request.session['best_route_by_time'] = best_route_by_time
    request.session['best_route_by_distance'] = best_route_by_distance
    return redirect(f"{reverse('refill:choose_option')}?vehicle_id={vehicle_id}&trip_id={trip_id}")

def format_duration(minutes):
    if minutes > 60 * 24:
        return f"{minutes // 1440} days {(minutes % 1440) // 60} hours {round(minutes % 60)} minutes"
    elif minutes > 59.5:
        return f"{round(minutes // 60)} hours {round(minutes % 60)} minutes"
    elif minutes < 1.5:
        return "1 minute"
    else:
        return f"{round(minutes % 60)} minutes"

def choose_option(request):
    vehicle_id = request.GET.get('vehicle_id')
    trip_id = request.GET.get('trip_id')
    best_route_by_time = request.session.get('best_route_by_time')
    best_route_by_distance = request.session.get('best_route_by_distance')
    # Summing and printing distances and durations
    if not best_route_by_time or not best_route_by_distance:
        return redirect(reverse('entry:load_data'))
    total_duration_by_distance=format_duration(sum(best_route_by_distance['durations']))
    total_duration_by_time=format_duration( sum(best_route_by_time['durations']))
    total_distance_by_distance=sum(best_route_by_distance['distances'])
    total_distance_by_time=sum(best_route_by_time['distances'])
    print("Total Distance (Best by Distance):", total_distance_by_distance)
    print("Total Duration (Best by Distance):", total_duration_by_distance)
    print("Total Distance (Best by Time):", total_distance_by_time)
    print("Total Duration (Best by Time):", total_duration_by_time)

    
        
    if request.method == 'POST':
        choice = request.POST.get('choice')
        if choice == 'time':
            selected_route = best_route_by_time
        else:
            selected_route = best_route_by_distance

        # Store the user's choice and redirect to results
        request.session['selected_route'] = selected_route
        return redirect(f"{reverse('refill:refill_amount')}?vehicle_id={vehicle_id}&trip_id={trip_id}")
        
    return render(request, 'refill/choose_option.html', {
        "by_time_duration": total_duration_by_time,
        "by_time_distance": f"{total_distance_by_time:.2f} km",
        "by_distance_duration": total_duration_by_distance,
        "by_distance_distance": f"{total_distance_by_distance:.2f} km",
    })

def update_trip(trip_id,vehicle_id,fuel_quantity,selected_route):
    print("yolo")
    
def refill_amount(request):
    vehicle_id = request.GET.get('vehicle_id')
    trip_id = request.GET.get('trip_id')
    selected_route = request.session.get('selected_route')
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle_data, id=vehicle_id)
    min_fuel=selected_route['distances'][-1]*float(vehicle.fuel_consumption_per_100km)/100
    max_fuel=float(vehicle.tank_size)
    if not selected_route:
        return redirect(reverse('entry:load_data'))

    if request.method == 'POST':
        fuel_quantity = request.POST.get('fuel_quantity')
        if fuel_quantity and fuel_quantity.isdigit():
            # Process the fuel refill amount (e.g., store in session or database)
            update_trip(trip_id,vehicle_id,fuel_quantity,selected_route)
            request.session['allowed_to_access_refill_views'] = True
            return redirect(f"{reverse('refill:results')}?vehicle_id={vehicle_id}&trip_id={trip_id}")
        else:
            error_message = "Please enter a valid fuel amount."
            return render(request, 'refill/fuel_amount.html', {'error_message': error_message})
    
    return render(request, 'refill/fuel_amount.html', {
        'vehicle_id': vehicle_id,
        'trip_id': trip_id,
        'min_value':min_fuel,
        'max_value':max_fuel,
    })
    




  

def results(request):
    if not request.session.get('allowed_to_access_refill_views', True):
        messages.error(request, "You are not authorized to access this page.")
        return redirect(reverse('refill:load_data'))
    
    request.session['allowed_to_access_refill_views'] = False

    try:
        vehicle_id,trip_id=scrape_query_paramaters(request.GET)
    except KeyError as e:
          messages.error(request, f"Invalid query parameters: {e}")
          logger.exception("Invalid query parameters:")
    except TypeError as e:
          messages.error(request, f"An unexpected error occurred: {e}")
          logger.exception("Unexpected Error:")
    
    trip = None
    vehicle = None

    if trip_id:
        trip = get_object_or_404(Trip, id=trip_id)
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle_data, id=vehicle_id)
        
    cost=trip.total_distance() / (100 / vehicle.fuel_consumption_per_100km) * vehicle.price_of_fuel
    
    trip.first_trip_node.trip_price=cost
    trip.first_trip_node.save()
    trip.save()
    total_distance = trip.total_distance()
    duration=format_duration( trip.total_duration())
    
        
    
    context = {
        "cost": f"{cost:.2f} {trip.main_currency()}",
        "duration": duration,
        "distance": f"{total_distance:.2f} km",
        "origin": trip.origin_address(),
        "destination": trip.destination_address(),
        "fuel_left":  f"{trip.refill_number+ vehicle.cur_fuel-vehicle.fuel_consumption_per_100km*total_distance/100:.2f} litres",
        "needs_refill": vehicle.need_refill(total_distance),
        "refill_price":  f"{ trip.refill_price:.2f} {trip.main_currency()}",
    }
    
    return render(request, "refill/results.html", context)




def scrape_query_paramaters(request_get):  
    
    #Args:
    #    request_get: A dictionary-like object containing query parameters.
    
    #Returns:
    #     A tuple containing (vehicle_id, trip_id).  Returns (None, None) if
    #     either parameter is missing. 
    
    #Raises:
    #    TypeError: If request_get is not a dictionary-like object.
  

    if not isinstance(request_get, dict):
        raise TypeError("request_get must be a dictionary-like object.")

    trip_id_param = request_get.get('trip_id', 'none') 
    vehicle_id_param = request_get.get('vehicle_id', 'none')
    

    if trip_id_param == None or vehicle_id_param == None:
        raise KeyError("Missing 'trip_id' or 'vehicle_id' query parameter.")
    
    vehicle_id=None if vehicle_id_param=='none' else int(vehicle_id_param)
    trip_id=None if trip_id_param=='none' else int(trip_id_param)
        

    return vehicle_id, trip_id

 
       
        
        
        