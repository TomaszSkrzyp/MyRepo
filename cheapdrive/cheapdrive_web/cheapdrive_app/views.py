
from django.http import HttpResponse,HttpResponseBadRequest
from .create_models import create_trip,create_vehicle
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from .models import  User
from .forms import UserRegistrationForm  # Import your custom form


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This creates and saves the user
            # ... add user to groups, send verification email, etc. ...
            messages.success(request, 'Registration successful!')
            return redirect('login')
        else:
            messages.error(request, 'Invalid registration information.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def visit(request):
    return HttpResponse("Hello dear user!!! I assume You would like to get some help in the road trip department. Thankfully, Cheapdrive is here with you.")   


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user is not None:
            
            login(request, user)
            
            messages.success(request, 'Login successful!')
            
            return redirect('load_data')  # Redirect to your home page
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')


def guest_access(request):
    request.session['is_guest'] = True  # Flag indicating guest session
    return redirect('load_data')  # Redirect to trip creation page



def validate_fuel_data(tank_size, cur_fuel, fuel_input_type, cur_fuel_percentage):
    """Validates fuel-related data."""
    if tank_size <= 0:
        raise ValidationError("Tank size must be positive.")
    if cur_fuel < 0:
        raise ValidationError("Current fuel cannot be negative.")
    if fuel_input_type == 'percentage':
        if not 0 <= cur_fuel_percentage <= 100:
            raise ValidationError("Fuel percentage must be between 0 and 100.")
 
from django.contrib.auth.forms import UserCreationForm



def load_data(request):

    if request.method == 'POST':
        try:
            starting_address = request.POST['starting_address']
            finishing_address = request.POST['finishing_address']
            tank_size = float(request.POST['tank_size'])
            fuel_type = request.POST['fuel_type']
            fuel_input_type = request.POST.get('fuel_input_type', 'amount') # Default to amount
            cur_fuel_percentage = float(request.POST['cur_fuel_percentage']) if fuel_input_type == 'percentage' else None
            cur_fuel = float(request.POST['cur_fuel']) if fuel_input_type == 'amount' else (cur_fuel_percentage / 100) * tank_size
            fuel_consumption_per_100km = float(request.POST['fuel_consumption_per_100km'])
            price_of_fuel = float(request.POST['price_of_fuel'])
            currency = request.POST['currency']

            validate_fuel_data(tank_size, cur_fuel, fuel_input_type, cur_fuel_percentage)

            if request.user.is_authenticated:
                
                user = request.user
                user = User.objects.get(pk=user.id)
                
                guest_id = None
            else:
                
                user = None
                guest_id = request.session.session_key or None
           
            print(f"Value of user: {user}")
            trip = create_trip(starting_address,finishing_address,user,guest_id)
            
            if trip:
                vehicle = create_vehicle(tank_size, fuel_type, cur_fuel, fuel_consumption_per_100km, price_of_fuel, currency, user, guest_id)
                if vehicle:
                    messages.success(request, "Data saved successfully!")
                    return redirect('success_page') # Replace with your URL name
                else:
                    messages.error(request, "Vehicle creation failed.")
            else:
                messages.error(request, "Trip creation failed.")

        except (KeyError, ValueError, ValidationError) as e:
            messages.error(request, f"Invalid input: {e}")
            return HttpResponseBadRequest(f"Invalid input: {e}")  # Better HTTP status
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")
            return HttpResponseBadRequest(f"Unexpected Error: {e}")
        
    return render(request, 'load_data.html')

def success_page(request):
    # Display a success message or redirect to another view
    return HttpResponse("Data received successfully!")


   

