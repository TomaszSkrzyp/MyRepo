from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import AbstractUser, Group, Permission,UserManager
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups'  # Unique related_name
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions'  # Unique related_name
    )
    objects = UserManager()

class Vehicle_data(models.Model):
    """
    Represents a user's vehicle with information about its fuel type, tank size,
    current fuel level, fuel consumption, purchase price, and currency.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    guest_session_id = models.CharField(max_length=255, null=True, blank=True)
    fuel_types = {
        "D": "Diesel",
        "P": "Pb95"
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
        max_length=3, 
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
        max_digits=4, 
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
            True if a refill is needed, False otherwise.
        """
        # Calculate fuel needed for the distance
        fuel_needed = (self.fuel_consumption_per_km * distance)/100

        # Check if current fuel is sufficient
        try:
            fuel_needed = (self.fuel_consumption_per_100km * distance) / 100
            return self.cur_fuel - fuel_needed < 0.1 * self.tank_size
        except ZeroDivisionError:
            return True

class Trip(models.Model):
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    guest_session_id = models.CharField(max_length=255, null=True, blank=True)
    starting_address = models.CharField(max_length=255)
    finishing_address = models.CharField(max_length=255)
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
    


    

    
    
    
        

# Create your models here.
