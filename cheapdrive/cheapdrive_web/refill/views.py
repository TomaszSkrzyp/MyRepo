from decimal import Decimal
import decimal
from sqlite3 import complete_statement
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

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

    


def validate_fuel_data(tank_size, cur_fuel, fuel_input_type, cur_fuel_percentage):
    """Validates fuel-related data."""
    if tank_size <= 0:
        raise ValidationError("Tank size must be positive.")
    if cur_fuel < 0:
        raise ValidationError("Current fuel cannot be negative.")
    if fuel_input_type == 'percentage':
        if not 0 <= cur_fuel_percentage <= 100:
            raise ValidationError("Fuel percentage must be between 0 and 100.")
 

logger = logging.getLogger(__name__) # Get a logger instance
@csrf_exempt
def load_data(request):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key is None:
        logger.critical("GOOGLE_API_KEY environment variable not set.")
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

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

                # Create trip and vehicle
                user = request.user if request.user.is_authenticated else None
                guest_id = request.session.session_key

                trip_id = create_trip(starting_address, finishing_address, user, guest_id)
                if trip_id:
                    vehicle_id = create_vehicle(tank_size, fuel_type, cur_fuel, fuel_consumption_per_100km, price_of_fuel, currency, trip_id)
                    if vehicle_id:
                        messages.success(request, "Data saved successfully!")
                        return redirect('refill:results_no_refill', vehicle_id=vehicle_id,trip_id=trip_id)  # Example duration

                    else:
                        messages.error(request, "Vehicle creation failed. Check your input data.")
                        logger.error("Vehicle creation failed.")
                else:
                    messages.error(request, "Trip creation failed. Check your input data.")
                    logger.error("Trip creation failed.")

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
        return render(request, 'refill/load_data.html', {'form': form, 'api_key': api_key})

    else:
        # Render empty form for GET requests
        form = LoadDataForm()
        return render(request, 'refill/load_data.html', {'form': form, 'api_key': api_key})




def results_no_refill(request, vehicle_id,trip_id):
    vehicle = get_object_or_404(Vehicle_data, id=vehicle_id)
    trip =  get_object_or_404(Trip, id=trip_id)
    cost=trip.distance / (100 / vehicle.fuel_consumption_per_100km) * vehicle.price_of_fuel
    print(cost,type(cost),type(trip.trip_price))
    trip.trip_price=cost
    trip.currency=vehicle.currency
    
    trip.save()
    
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
