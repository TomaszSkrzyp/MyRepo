
from importlib.metadata import requires
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from django.db.models import BooleanField
from entry.models import User
from django.contrib import messages


from django.contrib.gis.db import models as gis_models


class Vehicle_data(models.Model):
    """
    Represents a user's vehicle with information about its fuel type, tank size,
    current fuel level, fuel consumption, purchase price, and currency.
    """
    
    
    fuel_types = {
        "D": "Diesel",
        "PB95": "PB95",
        "LPG": "LPG",
        "PB98":"PB98"
    }
    
    tank_size = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0)],
        help_text="The size of the vehicle's fuel tank in liters."
    )
    fuel_type = models.CharField(
        max_length=4, 
        choices=fuel_types,
        help_text="The type of fuel used by the vehicle."
    )
    
    fuel_consumption_per_100km = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0)],
        help_text="The vehicle's fuel consumption in liters per 100 kilometer."
    )
    need_refill=BooleanField(
        null=True, 
        blank=True,
        
        help_text="Information wheter the vehicle needs refill."
    )
    
    
    
    
     # Optional relationship with User model, allowing guest users to not have this field set
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='vehicle_data', 
        help_text="The user who owns the vehicle."
    )

    


class TripNode(models.Model):
    origin=gis_models.PointField(
        geography=True,
        blank=True,
        null=True
    )
    destination=gis_models.PointField(
        geography=True,
        blank=True,
        null=True
    )
    
    distance = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.0)],
        help_text="Distance of trip"
    )
    duration = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.0)],
        help_text="Duration of the trip - in minutes"
    )
    currency = models.CharField(
        max_length=3,
        default='PLN',
        help_text="The currency of the purchase price."
    )
    bought_gas_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Price of bought fuel at the beginning of node. Per liter",
        blank=True,
        null=True,
    )
    fuel_refilled=models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=[MinValueValidator(0.0)],
        blank=True,
        null=True,
        help_text="Fuel added at the beggining of the node"
    )
    next_trip = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_node',
        help_text="Next trip node"
    )

    def delete(self, *args, **kwargs):
        # Update the previous node's next_trip to null before deleting this node
        if self.previous_node.exists():
            self.previous_node.update(next_trip=None)


        super().delete(*args, **kwargs)


class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    guest_session_id = models.CharField(max_length=255, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle_data, on_delete=models.CASCADE, null=True, blank=True, related_name='trip')
    
    origin_address = models.CharField(max_length=255, blank=True)
    destination_address = models.CharField(max_length=255, blank=True)

   
    
    first_trip_node = models.ForeignKey(
        TripNode,
        on_delete=models.CASCADE,  # Cascade deletes all trip nodes starting from this
        default=None,
        related_name='trips',
        help_text="First trip node in this trip"
    )
    def clean(self):
        """Ensure data integrity: Every Trip must have a first_trip_node."""
        if not self.first_trip_node:
            raise ValidationError("A trip must have at least one trip node as its starting point.")
        
    
    def main_currency(self):
        return self.first_trip_node.currency
    
    def total_distance(self):
        """Calculate the total distance of the trip."""
        distance = 0
        current_node = self.first_trip_node
        while current_node:
            distance += current_node.distance
            current_node = current_node.next_trip
        return distance

    def total_duration(self):
        """Calculate the total duration of the trip."""
        duration = 0
        current_node = self.first_trip_node
        while current_node:
            duration += current_node.duration
            current_node = current_node.next_trip
        return duration

    def total_price_bought_and_used(self):#TO CHANGE- przeliczenie walut
        """Calculate the total price of the trip."""
        price_used = 0
        current_node = self.first_trip_node
        price_bought=-current_node.bought_gas_price*current_node.fuel_refilled
        while current_node.next_trip:
            price_used += current_node.bought_gas_price*current_node.fuel_refilled
            current_node = current_node.next_trip
        price_bought+=price_used+current_node.bought_gas_price*current_node.fuel_refilled
        price_used += current_node.distance * self.vehicle.fuel_consumption_per_100km / 100 * current_node.bought_gas_price

        return (round(price_bought,2),round(price_used))
    
    def fuel_left(self):
        """Calculate fuel left after the trip."""
        all_fuel_refilled=0
        current_node = self.first_trip_node
        
        while current_node.next_trip:
            all_fuel_refilled+=current_node.fuel_refilled
            current_node = current_node.next_trip
        return all_fuel_refilled+current_node.fuel_refilled-current_node.distance*self.vehicle.fuel_consumption_per_100km/100
        
        

   
    def save(self, *args, **kwargs):
        """Override save to ensure clean method is called."""
        self.clean()
        super().save(*args, **kwargs)




    