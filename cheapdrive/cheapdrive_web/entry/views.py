
from secrets import token_bytes
from django.http import HttpResponse,HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

from refill.models import Trip,TripNode,Vehicle_data

from .forms import UserRegistrationForm  
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from refill.models import Trip
from .database_updates import update_brand_prices,update_station_objects

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This creates and saves the user
            # ... add user to groups, send verification email, etc. ...
            messages.success(request, 'Registration successful!')
            return redirect('entry:login')
        else:
            messages.error(request, 'Invalid registration information.')
    else:
        form =UserRegistrationForm()
    context = {'form': form}
    return render(request, 'entry/register.html', context)

def visit(request):
    #update_brand_prices();update_station_objects()
    deleted_count1, _ = Trip.objects.all().delete()
    deleted_count2, _ = TripNode.objects.all().delete()
    deleted_count3, _ = Vehicle_data.objects.all().delete()
    
    return render(request, 'entry/visit.html')


def login_view(request):
    if request.user.is_authenticated:
        print("wtf")
        return redirect('entry:logout')  
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                next_url = request.GET.get('next', 'entry:logged')  # Redirect to 'next' or default to 'logged'
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = AuthenticationForm()
        if 'next' in request.GET:
            messages.error(request, 'You must be logged in to access that page.')

    context = {'form': form}
    response = render(request, 'entry/login.html', context)

    # Prevent browser from caching the page
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


def logout_view(request):
    logout(request)
    
    messages.success(request, 'You have been logged out successfully.')
    return redirect('entry:visit')


def guest_access(request):
    request.session['is_guest'] = True  # Flag indicating guest session
    return redirect(f"{reverse('refill:load_data')}?vehicle_id=none&trip_id=none")  # Redirect to trip creation page

@login_required(login_url='/login/')
def logged_view(request):
    """
    View that allows users to either view trip history or set up a new trip.
    """
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'history':
            return redirect('entry:trip_history')  # URL name for trip history
        elif action == 'user_vehicles':
             return redirect('entry:user_vehicles')
            
        elif action == 'new_trip':
          return redirect(f"{reverse('refill:load_data')}?vehicle_id=none&trip_id=none")
        
            
        elif action == 'logout':
            return redirect('entry:logout')  # URL name for setting up a new trip
        elif action not in ['history', 'new_trip', 'logout']:
            messages.error(request, "Invalid action selected.")
            return redirect('entry:logged')
        
    return render(request, 'entry/logged.html')



@login_required(login_url='/login/')
def trip_history_view(request):
    # Retrieve trips for the logged-in user, ordered by distance in descending order
    trips = Trip.objects.filter(user=request.user).order_by('-first_trip_node_id')
    
    trip_data = []
    for trip in trips:
        vehicle = trip.vehicle
        total_distance=trip.total_distance()
        refill_needed = vehicle.need_refill 
            
        
        trip_data.append({
            'origin_address':trip.origin_address,
            'destination_address':trip.destination_address,
            'total_distance':total_distance,
            'total_duration':trip.total_duration(),
            'total_price':trip.total_price_bought_and_used()[0],
            'currency':trip.main_currency(),
            'trip_id':trip.id,
        })

    context = {
        'trip_data': trip_data,
    }
    
    return render(request, 'entry/trip_history.html', context)
@login_required
def user_vehicles_view(request):
    # Get all vehicles for the logged-in user
    vehicles = request.user.vehicle_data.all()
    
    return render(request, 'entry/user_vehicles.html', {'vehicles': vehicles})

