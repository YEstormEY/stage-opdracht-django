import csv
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from hotels.models import City, Hotel
import os

class Command(BaseCommand):
    help = "Import data from city.csv and hotel.csv"

    def handle(self, *args, **kwargs):
        self.import_cities()
        self.import_hotels()

    def import_cities(self):
        # Path to city.csv in the root 'csv' directory
        csv_file_path = os.path.join('csv', 'city.csv')
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                try:
                    # Ensure the row has the expected number of columns
                    if len(row) >= 2:
                        City.objects.create(code=row[0], name=row[1])
                        self.stdout.write(self.style.SUCCESS(f'Imported city: {row[1]}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Skipped malformed row: {row}'))
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(f'Skipped duplicate city: {row[1]}'))

    def import_hotels(self):
        # Path to hotel.csv in the root 'csv' directory
        csv_file_path = os.path.join('csv', 'hotel.csv')
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                try:
                    # Ensure the row has the expected number of columns
                    if len(row) >= 3:
                        city = City.objects.get(code=row[0])
                        Hotel.objects.create(city=city, code=row[1], name=row[2])
                        self.stdout.write(self.style.SUCCESS(f'Imported hotel: {row[2]}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Skipped malformed row: {row}'))
                except City.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'City not found for hotel: {row[2]}'))
                except IntegrityError:
                    self.stdout.write(self.style.WARNING(f'Skipped duplicate hotel: {row[2]}'))
