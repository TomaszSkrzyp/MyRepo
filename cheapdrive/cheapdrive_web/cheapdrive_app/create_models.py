from api_calls.google_api_calls import address_validation_and_distance
from api_calls.api_exceptions import AddressError
from .models import Vehicle_data,Trip
from django.core.exceptions import ValidationError

def create_trip(start, finish,user,guest_id):
    try:
        trip_distance,trip_duration=address_validation_and_distance(start,finish)
        Trip.objects.create(
            user=user,
            guest_session_id=guest_id,
            starting_address=start,
            finishing_address=finish,
            distance=trip_distance,
            duration=trip_duration,
        )
        return True
    
    except AddressError as e:
        #handle bad addreses
        print(f"Adress Error: {e}")
        return False  # Or raise the exception
        
        
    except ValidationError as e:
        # Handle validation errors appropriately (log, raise, return error message)
        print(f"Validation Error: {e}")
        return False  # Or raise the exception
def create_vehicle(tank_size, fuel_type, cur_fuel, fuel_consumption_per_100km, price_of_fuel, currency,user,guest_id):
    """Creates a user_data model instance with validation."""
    
    try:
           Vehicle_data.objects.create(
            tank_size=tank_size,
            fuel_type=fuel_type,
            cur_fuel=cur_fuel,
            fuel_consumption_per_100km=fuel_consumption_per_100km,
            price_of_fuel= price_of_fuel,
            currency=currency,
            user=user,
            guest_session_id=guest_id,
            )
           return True
    except ValidationError as e:
        # Handle validation errors appropriately (log, raise, return error message)
        print(f"Validation Error: {e}")
        return False # Or raise the exception
    