from django.urls import path
from .api_views import city_list, hotel_list
from .views import CityView, HotelInCityView

urlpatterns = [
    path('api/cities/', city_list, name='api_city_list'),
    path('api/hotels/<str:code>', hotel_list, name='api_hotel_list'),
]