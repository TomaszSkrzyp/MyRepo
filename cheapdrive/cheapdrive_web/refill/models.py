
from importlib.metadata import requires
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from entry.models import User
from django.contrib import messages


class Vehicle_data(models.Model):
    """
    Represents a user's vehicle with information about its fuel type, tank size,
    current fuel level, fuel consumption, purchase price, and currency.
    """
    
    
    fuel_types = {
        "D": "Diesel",
        "PB95": "PB95",
        "LPG": "LPG",
        "PB98":"PB95"
    }
    class Meta:
        constraints = [
        models.CheckConstraint(
            name="cur_fuel_lte_tank_size",
            check=models.Q(cur_fuel__lte=models.F("tank_size")),
        )
    ]
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
    cur_fuel = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0)],
        help_text="The current amount of fuel in the tank in liters."
    )
    fuel_consumption_per_100km = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0)],
        help_text="The vehicle's fuel consumption in liters per kilometer."
    )
    price_of_fuel = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        validators=[MinValueValidator(0.0)],
        help_text="The price the stored gas was purchased for."
    )
    currency = models.CharField(
        max_length=3, 
        default='PLN',
        help_text="The currency of the purchase price."
    )
    
    def need_refill(self, distance):
        """
        Checks if the vehicle needs a refill based on distance and fuel consumption.

        Args:
            distance: The distance to be traveled.

        Returns:
            True if a refill is needed, False otherwise.  Returns True if fuel consumption is invalid.
        """
        if self.fuel_consumption_per_100km <= 0:
            return True #Invalid Fuel Consumption

        fuel_needed = (self.fuel_consumption_per_100km * distance) / 100

        #Check for negative fuel values (Should be prevented in data validation)
        if self.cur_fuel < 0 or self.tank_size < 0:
            return True # Invalid fuel data

        return self.cur_fuel - fuel_needed < 0.1 * float(self.tank_size)
    
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
    origin_address = models.CharField(max_length=255)
    destination_address = models.CharField(max_length=255)
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
    trip_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Price of the trip",
        default=0
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
    refill_price=models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Price of fuel bought on trip",
        default=0
    )
    refill_number=models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text="Litres of gas refilled during trip",
        default=0
    )
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

    def total_price(self):#TO CHANGE- przeliczenie walut
        """Calculate the total price of the trip."""
        price = 0
        current_node = self.first_trip_node
        while current_node:
            price += current_node.trip_price
            current_node = current_node.next_trip
        return price

    def origin_address(self):
        """Retrieve the starting address of the trip."""
        if self.first_trip_node:
            return self.first_trip_node.origin_address
        return None

    def destination_address(self):
        """Retrieve the finishing address of the trip."""
        current_node = self.first_trip_node
        if not current_node:
            return None
        while current_node.next_trip:
            current_node = current_node.next_trip
        return current_node.destination_address

    def save(self, *args, **kwargs):
        """Override save to ensure clean method is called."""
        self.clean()
        super().save(*args, **kwargs)




    