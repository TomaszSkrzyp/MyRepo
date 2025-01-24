from api_calls.google_api_calls import address_validation_and_distance
from api_calls.api_exceptions import AddressError
from api_calls.api_calculations import get_coordinates
from .models import Vehicle_data,Trip,TripNode
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.db import transaction

def create_trip(origin, destination,currency, user, guest_id,vehicle_id,cur_fuel,price_of_fuel):
    try:
        # Validate addresses and calculate distance/duration. Include addreses corrected by Google api
        trip_distance, trip_duration,corrected_origin,corrected_destination = address_validation_and_distance(origin, destination)
        if trip_distance is None or trip_duration is None:
            raise ValueError("Failed to calculate trip details.")
       
        # GIS Point (longitude, latitude)
        try:
            origin_location = Point(get_coordinates(origin))
        
            destination_location = Point(get_coordinates(destination))
        except Exception as e:
            print(f"Error fetching coordinates: {e}")
            return None
        # Use atomic transactions to ensure consistent database state
        with transaction.atomic():
            # Create the first TripNode
            first_node = TripNode.objects.create(
                origin=origin_location,
                destination=destination_location,
                distance=trip_distance,
                currency=currency,
                duration=trip_duration,  
                fuel_refilled=cur_fuel,
                bought_gas_price=price_of_fuel,
            )

            # Create the Trip and link it to the first TripNode
            trip = Trip.objects.create(
                origin_address=corrected_origin,
                destination_address=corrected_destination,
                user=user,
                guest_session_id=guest_id,
                first_trip_node=first_node,
                vehicle = Vehicle_data.objects.select_for_update().get(pk=vehicle_id)
,
            )

        return trip.id

    except AddressError as e:
        raise e
        
        
    except ValidationError as e:
        raise e

def create_vehicle(tank_size, fuel_type, fuel_consumption_per_100km):
    """Creates a user_data model instance with validation."""
    
    try: 
           vehicle=Vehicle_data.objects.create(
            tank_size=tank_size,
            fuel_type=fuel_type,
            fuel_consumption_per_100km=fuel_consumption_per_100km,
            
            
            )
           return vehicle.id
    except ValidationError as e:
        # Handle validation errors appropriately (log, raise, return error message)
        print(f"Validation Error: {e}")
        return None # Or raise the exception
    