from django.urls import path
from .views import CityView, HotelInCityView

urlpatterns = [
    path('cities/', CityView.as_view(), name='city_list'),
    path('hotels/', HotelInCityView.as_view(), name='hotel_in_city'),
]