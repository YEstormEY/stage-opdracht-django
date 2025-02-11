from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Hotel, City

# Create your views here.

# City view
class CityView(TemplateView):
    template_name = 'hotels/city_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cities'] = City.objects.all()  # Instead of values()
        return context




# Hotel view
class HotelView(TemplateView):
    template_name = 'hotels/hotel_list.html'
    
    def get_context_data(self, **kwargs):
        # Get the default context data from the parent class.
        context = super().get_context_data(**kwargs)
        # Query all hotels from the database.
        context['hotels'] = Hotel.objects.all()
        return context
    

# View to display hotels for selected city
class HotelInCityView(TemplateView):
    template_name = 'hotels/hotel_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.GET)  # Debugging print statement
        # Get the city code from the URL parameter.
        city = self.request.GET.get('city')
        
        if city:
            # Filter hotels by the related City's code.
            context['hotels'] = Hotel.objects.filter(city__code=city)
            context['selected_city'] = City.objects.filter(code=city).first()
        else:
            # Show all hotels if no city is provided.
            context['hotels'] = Hotel.objects.all()
            context['selected_city'] = None  # or assign a default value if desired
        return context

