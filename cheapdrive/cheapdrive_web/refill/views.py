from decimal import Decimal
import decimal
from django.shortcuts import get_object_or_404, render,redirect
from .models import Vehicle_data,Trip
from entry.models import  User
from django.core.exceptions import ValidationError
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib import messages
from .create_models import create_trip,create_vehicle
from .forms import LoadDataForm
import os
import logging

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

    


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
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key is None:
        logger.critical("GOOGLE_API_KEY environment variable not set.")
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    # Extract query parameters
    trip_id_param = request.GET.get('trip_id', 'none')
    vehicle_id_param = request.GET.get('vehicle_id', 'none')

    # Convert query parameters to appropriate values
    trip_id = None if trip_id_param == 'none' else int(trip_id_param)
    vehicle_id = None if vehicle_id_param == 'none' else int(vehicle_id_param)

    # Initialize existing trip or vehicle if IDs are provided
    trip = None
    vehicle = None

    if trip_id:
        trip = get_object_or_404(Trip, id=trip_id)
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle_data, id=vehicle_id)

    if request.method == 'POST':
        form = LoadDataForm(request.POST)
        if form.is_valid():
            try:
                # Extract form data
                starting_address = form.cleaned_data['starting_address']
                finishing_address = form.cleaned_data['finishing_address']
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

                # Use existing trip or create a new one
                if not trip:
                    user = request.user if request.user.is_authenticated else None
                    guest_id = request.session.session_key
                    trip_id = create_trip(starting_address, finishing_address, user, guest_id)
                    trip = Trip.objects.get(id=trip_id)  # Retrieve the created Trip object

                # Use existing vehicle or create a new one
                if not vehicle:
                    vehicle_id = create_vehicle(tank_size, fuel_type, cur_fuel, fuel_consumption_per_100km, price_of_fuel, currency, trip.id)
                  
                    vehicle = Vehicle_data.objects.get(id=vehicle_id)  # Retrieve the created Vehicle object
                    if request.user.is_authenticated:
                        
                        vehicle.user = request.user
                        vehicle.save()

                messages.success(request, "Data saved successfully!")
                
                return redirect(f"{reverse('refill:results_no_refill')}?vehicle_id={vehicle_id}&trip_id={trip_id}")

            except ValidationError as e:
                messages.error(request, f"Validation Error: {e}")
                logger.exception("Validation Error:")
            except (KeyError, ValueError) as e:
                messages.error(request, f"Invalid input: {e}")
                logger.exception("Invalid Input Error:")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
                logger.exception("Unexpected Error:")

        # Re-render form with errors and original data
        return render(request, 'refill/load_data.html', {
            'vehicle_id': vehicle.id if vehicle else None,
            'trip_id': trip.id if trip else None,
            'form': form,
            'api_key': api_key
        })

    else:
        # Render form pre-filled with existing trip or vehicle data if provided
        initial_data = {}
        if trip:
            initial_data.update({
                'starting_address': trip.starting_address,
                'finishing_address': trip.finishing_address,
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
            'api_key': api_key
        })



def results_no_refill(request):
    trip_id_param = request.GET.get('trip_id', 'none')
    vehicle_id_param = request.GET.get('vehicle_id', 'none')

    # Convert query parameters to appropriate values
    trip_id = None if trip_id_param == 'none' else int(trip_id_param)
    vehicle_id = None if vehicle_id_param == 'none' else int(vehicle_id_param)

    # Initialize existing trip or vehicle if IDs are provided
    trip = None
    vehicle = None

    if trip_id:
        trip = get_object_or_404(Trip, id=trip_id)
    if vehicle_id:
        vehicle = get_object_or_404(Vehicle_data, id=vehicle_id)
        
    cost=trip.distance / (100 / vehicle.fuel_consumption_per_100km) * vehicle.price_of_fuel
    vehicle.trip_price=cost
    
    vehicle.save()
    
    context = {
        "cost": f"{cost:.2f} {vehicle.currency}",
        "duration": f"{trip.duration:.2f} minutes",
        "distance": f"{trip.distance:.2f} km",
        "start": trip.starting_address,
        "destination": trip.finishing_address,
        "fuel_left": vehicle.cur_fuel-vehicle.fuel_consumption_per_100km*trip.distance/100,
        "needs_refill": vehicle.need_refill(trip.distance),
        
    }
    
    return render(request, "refill/no_refill_results.html", context)
