from django.contrib import admin
from .models import City, Hotel

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')  # Fields to display in the list view
    search_fields = ('name', 'code')  # Fields to enable searching
    ordering = ('name',)  # Default ordering

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city')  # Fields to display in the list view
    list_filter = ('city',)  # Filter hotels by city
    search_fields = ('name', 'code')  # Fields to enable searching
    ordering = ('city', 'name')  # Default ordering
