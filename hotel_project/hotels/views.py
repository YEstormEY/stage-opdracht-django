from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Hotel

# Create your views here.

# Hotel view
class HotelView(TemplateView):
    template_name = 'hotels/hotel_list.html'
    
    def get_context_data(self, **kwargs):
        # Get the default context data from the parent class.
        context = super().get_context_data(**kwargs)
        # Query all hotels from the database. You can adjust the query to add filtering or ordering.
        context['hotels'] = Hotel.objects.all()
        return context
