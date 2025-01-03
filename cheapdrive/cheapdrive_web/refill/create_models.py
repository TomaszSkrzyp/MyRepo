from api_calls.google_api_calls import address_validation_and_distance
from api_calls.api_exceptions import AddressError
from .models import Vehicle_data,Trip
from django.core.exceptions import ValidationError

def create_trip(start, finish,user,guest_id):
    try:
        trip_distance,trip_duration=address_validation_and_distance(start,finish)
        trip=Trip.objects.create(
            user=user,
            guest_session_id=guest_id,
            starting_address=start,
            finishing_address=finish,
            distance=trip_distance,
            duration=trip_duration,
        )
        return trip.id
    
    except AddressError as e:
        #handle bad addreses
        raise e
        return None  # Or raise the exception
        
        
    except ValidationError as e:
        # Handle validation errors appropriately (log, raise, return error message)
        raise e
        return None  # Or raise the exception
def create_vehicle(tank_size, fuel_type, cur_fuel, fuel_consumption_per_100km, price_of_fuel, currency,trip_id):
    """Creates a user_data model instance with validation."""
    
    try:
           trip = Trip.objects.get(pk=trip_id)   
           vehicle=Vehicle_data.objects.create(
            tank_size=tank_size,
            fuel_type=fuel_type,
            cur_fuel=cur_fuel,
            fuel_consumption_per_100km=fuel_consumption_per_100km,
            price_of_fuel= price_of_fuel,
            currency=currency,
            trip=trip
            )
           return vehicle.id
    except ValidationError as e:
        # Handle validation errors appropriately (log, raise, return error message)
        print(f"Validation Error: {e}")
        return False # Or raise the exception
    