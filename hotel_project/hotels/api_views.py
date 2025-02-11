from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import City, Hotel

@api_view(['GET'])
def city_list(request):
    cities = City.objects.values()
    return Response(cities)

@api_view(['GET'])
def hotel_list(request, code):
    hotels = Hotel.objects.filter(city__code=code).values()
    return Response(hotels)