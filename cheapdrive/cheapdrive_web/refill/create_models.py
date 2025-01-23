from api_calls.google_api_calls import address_validation_and_distance
from api_calls.api_exceptions import AddressError
from .models import Vehicle_data,Trip,TripNode
from django.core.exceptions import ValidationError

from django.db import transaction

def create_trip(origin, destination,currency, user, guest_id,vehicle_id):
    try:
        # Validate addresses and calculate distance/duration. Include addreses corrected by Google api
        trip_distance, trip_duration,corrected_origin,corrected_destination = address_validation_and_distance(origin, destination)

        # Use atomic transactions to ensure consistent database state
        with transaction.atomic():
            # Create the first TripNode
            first_node = TripNode.objects.create(
                origin_address=corrected_origin,
                destination_address=corrected_destination,
                distance=trip_distance,
                currency=currency,
                duration=trip_duration,  
            )

            # Create the Trip and link it to the first TripNode
            trip = Trip.objects.create(
                user=user,
                guest_session_id=guest_id,
                first_trip_node=first_node,
                vehicle=Vehicle_data.objects.get(pk=vehicle_id),
            )

        return trip.id

    except AddressError as e:
        raise e
        return None  # Or raise the exception
        
        
    except ValidationError as e:
        raise e
        return None  # Or raise the exception 

def create_vehicle(tank_size, fuel_type, cur_fuel, fuel_consumption_per_100km, price_of_fuel, currency):
    """Creates a user_data model instance with validation."""
    
    try: 
           vehicle=Vehicle_data.objects.create(
            tank_size=tank_size,
            fuel_type=fuel_type,
            cur_fuel=cur_fuel,
            fuel_consumption_per_100km=fuel_consumption_per_100km,
            price_of_fuel= price_of_fuel,
            currency=currency,
            
            )
           return vehicle.id
    except ValidationError as e:
        # Handle validation errors appropriately (log, raise, return error message)
        print(f"Validation Error: {e}")
        return None # Or raise the exception
    