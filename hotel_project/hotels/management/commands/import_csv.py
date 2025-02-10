import csv
import io
import requests
from django.core.management.base import BaseCommand
from hotels.models import City, Hotel

class Command(BaseCommand):
    """
    Management command for importing CSV data into the City and Hotel models.
    
    This command supports two modes:
        - "http" mode: fetches CSV files via authenticated HTTP
        - "file" mode: reads local CSV files
        
    The expected CSV format is:
      - City CSV:  CITY_CODE;NAME
      - Hotel CSV: CITY_CODE;HOTEL_CODE;NAME
      
    Usage Examples:
      - Import data via HTTP:
          python manage.py import_csv --mode=http \
              --city-url="http://example.com/city.csv" \
              --hotel-url="http://example.com/hotel.csv"
      
      - Import data from local files:
          python manage.py import_csv --mode=file \
              --city-path="/path/to/city.csv" \
              --hotel-path="/path/to/hotel.csv"
    """
    help = 'Import CSV data for City and Hotel models'

    def add_arguments(self, parser):
        """
        Add custom command arguments to the parser.
        
        Args:
            parser (argparse.ArgumentParser): The argument parser used to parse command options.
        """
        parser.add_argument(
            '--mode',
            type=str,
            choices=['http', 'file'],
            default='http',
            help='Import mode: "http" to fetch CSV files via authenticated HTTP, "file" to read local CSV files'
        )
        parser.add_argument(
            '--city-url',
            type=str,
            help='URL for city CSV (used in HTTP mode)'
        )
        parser.add_argument(
            '--hotel-url',
            type=str,
            help='URL for hotel CSV (used in HTTP mode)'
        )
        parser.add_argument(
            '--city-path',
            type=str,
            help='Local file path for city CSV (used in file mode)'
        )
        parser.add_argument(
            '--hotel-path',
            type=str,
            help='Local file path for hotel CSV (used in file mode)'
        )

    def handle(self, *args, **kwargs):
        """
        Main command handler that triggers the CSV import based on the provided options.
        
        Args:
            *args: positional arguments
            **kwargs: Command-line arguments including mode, city URL/PATH, and hotel URL/PATH
        """
        # Retrieve the options dictionary
        options = kwargs
        mode = options.get('mode')

        if mode == 'http':
            self.stdout.write("Importing via authenticated HTTP...")
            city_url = options.get('city_url')
            hotel_url = options.get('hotel_url')
            # Hardcoded credentials for demo purposes
            auth = ('python-demo', 'claw30_bumps')
            if city_url:
                self.import_cities_from_url(city_url, auth)
            if hotel_url:
                self.import_hotels_from_url(hotel_url, auth)
        else:
            self.stdout.write("Importing from local files...")
            city_path = options.get('city_path')
            hotel_path = options.get('hotel_path')  # Changed key to 'hotel_path' for consistency
            if city_path:
                self.import_cities_from_file(city_path)
            if hotel_path:
                self.import_hotels_from_file(hotel_path)

        self.stdout.write(self.style.SUCCESS('CSV import complete'))

    def import_cities_from_url(self, url, auth):
        """
        Fetches and imports city data from a CSV file via an HTTP request.
        
        Args:
            url (str): The URL of the city CSV file.
            auth (tuple): A tuple containing the username and password for HTTP basic authentication
        """
        try:
            response = requests.get(url, auth=auth)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            content = response.content.decode('utf-8')
            self.import_cities_from_string(content)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching city CSV: {e}"))

    def import_hotels_from_url(self, url, auth):
        """
        Fetches and imports hotel data from a CSV file via an HTTP request.
        
        Args:
            url (str): The URL of the hotel CSV file.
            auth (tuple): A tuple containing the username and password for HTTP basic authentication
        """
        try:
            response = requests.get(url, auth=auth)
            response.raise_for_status()
            content = response.content.decode('utf-8')
            self.import_hotels_from_string(content)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error fetching hotel CSV: {e}"))

    def import_cities_from_file(self, path):
        """
        Reads and imports city data from a local CSV file.
        
        Args:
            path (str): The local file path of the city CSV file.
        """
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
            self.import_cities_from_string(content)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading city CSV file: {e}"))

    def import_hotels_from_file(self, path):
        """
        Reads and imports hotel data from a local CSV file.
        
        Args:
            path (str): The local file path of the hotel CSV file.
        """
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
            self.import_hotels_from_string(content)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading hotel CSV file: {e}"))
            
    def import_cities_from_string(self, csv_string):
        """
        Parses a CSV string and imports each valid row as a new City.

        Args:
            csv_string (str): The CSV data as a string.
            
        Expected CSV Format:
            CITY_CODE;NAME
        """
        reader = csv.reader(io.StringIO(csv_string), delimiter=';')
        imported_count = 0
        skipped_count = 0
        for idx, row in enumerate(reader, start=1):
            if not row or len(row) != 2:
                self.stdout.write(self.style.WARNING(f"Skipping row {idx}: invalid format"))
                skipped_count += 1
                continue
            code, name = row
            if not code or not name:
                self.stdout.write(self.style.WARNING(f"Skipping row {idx}: missing values"))
                skipped_count += 1
                continue
            if City.objects.filter(code=code).exists():
                self.stdout.write(self.style.WARNING(f"Row {idx}: City code {code} already exists"))
                skipped_count += 1
                continue
            City.objects.create(code=code, name=name)
            imported_count += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {imported_count} cities, skipped {skipped_count} rows"))

    def import_hotels_from_string(self, csv_string):
        """
        Parses a CSV string and imports each valid row as a new Hotel, linking it to its City.

        Args:
            csv_string (str): The CSV data as a string.
            
        Expected CSV Format:
            CITY_CODE;HOTEL_CODE;NAME
        """
        reader = csv.reader(io.StringIO(csv_string), delimiter=';')
        imported_count = 0
        skipped_count = 0
        for idx, row in enumerate(reader, start=1):
            if not row or len(row) != 3:
                self.stdout.write(self.style.WARNING(f"Skipping row {idx}: invalid format"))
                skipped_count += 1
                continue
            city_code, hotel_code, name = row
            try:
                city = City.objects.get(code=city_code)
            except City.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Row {idx}: City {city_code} not found"))
                skipped_count += 1
                continue
            if not hotel_code or not name:
                self.stdout.write(self.style.WARNING(f"Skipping row {idx}: missing hotel code or name"))
                skipped_count += 1
                continue
            if Hotel.objects.filter(code=hotel_code, city=city).exists():
                self.stdout.write(self.style.WARNING(f"Row {idx}: Hotel code {hotel_code} already exists for this city"))
                skipped_count += 1
                continue
            Hotel.objects.create(code=hotel_code, name=name, city=city)
            imported_count += 1
        self.stdout.write(self.style.SUCCESS(f"Imported {imported_count} hotels, skipped {skipped_count} rows"))
