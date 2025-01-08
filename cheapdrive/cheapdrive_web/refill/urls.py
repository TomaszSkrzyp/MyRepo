from django.urls import path
from . import views 

app_name = 'refill' 
urlpatterns = [
     path('no_refill/', views.results_no_refill, name='results_no_refill'),
    #for using idspath('load_data/<int:vehicle_id>/<int:trip_id>/', views.load_data, name='load_data'),
    path('load_data/', views.load_data, name='load_data'),
    # ... other URL patterns ...
]