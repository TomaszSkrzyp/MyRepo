
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include,path

urlpatterns = [
    path("cheapdrive/",
    include("cheapdrive_app.urls")),
    path('admin/', admin.site.urls),
    
    #path("refill/",
    #include("refill.urls")),
]
urlpatterns += staticfiles_urlpatterns()

