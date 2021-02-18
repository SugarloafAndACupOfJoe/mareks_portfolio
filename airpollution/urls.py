from django.urls import path
from . import views

app_name = 'airpollution'

urlpatterns = [
    path('', views.airpollution, name='airpollution'),
    path('temp_country_creator', views.temp_country_creator, name='temp_country_creator'),
    path('temp_add_colors_to_pollutants', views.temp_add_colors_to_pollutants, name='temp_add_colors_to_pollutants'),
]
