from django.urls import path
from . import views


urlpatterns = [
    path("", views.visit, name="visit"),
    path('login/', views.login_view, name='login'),
    path('guest/', views.guest_access, name='guest_access'),
    path('load_data/', views.load_data, name='load_data'),
    path('success_page/', views.success_page, name='success_page'),
    path('register/', views.register, name='register'),
    ##path('protected/', views.my_protected_view, name='protected'),  
]
