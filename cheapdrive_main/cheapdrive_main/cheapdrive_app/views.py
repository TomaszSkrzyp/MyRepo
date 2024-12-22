from django.shortcuts import render
from django.http import HttpResponse

def visit_message(request):
    return HttpResponse("Hello dear user!!! I assume You would like to get some help in the road trip department. Thankfully, Cheapdrive is here with you.")   
    
def print_route_parameters(distance, duration,request):
    """Prints distance and duration in a user-friendly format on one line.

    Args:
        distance: Distance in kilometers.
        duration: Duration in seconds.
    """
    remaining_time = duration
    time_measures = []
    time_measures_displayed=0
    if (remaining_time>=86400) & (time_measures_displayed<2):  # 1 day = 86400 seconds
        days = remaining_time // 86400
        time_measures.append(f"{days} {'day' if days == 1 else 'days'}")
        remaining_time %= 86400
        time_measures_displayed+=1

    if (remaining_time>= 3600) & (time_measures_displayed<2):  # 1 hour = 3600 seconds
        hours = remaining_time // 3600
        time_measures.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
        remaining_time %= 3600
        
        time_measures_displayed+=1

    if (remaining_time>= 60) & (time_measures_displayed<2):  # 1 minute = 60 seconds
        minutes = remaining_time // 60
        time_measures.append(f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
        remaining_time %= 60
        
        time_measures_displayed+=1

    if (remaining_time>0) & (time_measures_displayed<1):
        time_measures.append("1 minute")
            
        time_measures_displayed+=1

    return HttpResponse  (f"Distance of this route: {round(distance)} kilometers, Duration: {' '.join(time_measures)}")
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.
