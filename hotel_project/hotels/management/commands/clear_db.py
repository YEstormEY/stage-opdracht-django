from django.core.management.base import BaseCommand
from hotels.models import City, Hotel

class Command(BaseCommand):
    help = 'Clears the database'

    def handle(self, *args, **options):
        Hotel.objects.all().delete()
        City.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database cleared'))