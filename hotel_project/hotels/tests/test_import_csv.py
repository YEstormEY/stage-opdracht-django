from io import StringIO
from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase
from hotels.models import City, Hotel
from hotels.management.commands.import_csv import Command
import os
from tempfile import NamedTemporaryFile

class ImportCSVTests(TestCase):
    def setUp(self):
        # Clear database data before every test.
        City.objects.all().delete()
        Hotel.objects.all().delete()
            
    def test_import_cities_from_string_valid_data(self):
        csv_data = "AMS;Amsterdam\nBCN;Barcelona\n"
        out = StringIO()
        
        command = Command()
        command.stdout = out
        command.import_cities_from_string(csv_data)
        
        self.assertEqual(City.objects.count(), 2)
        self.assertIn("Imported 2 cities, skipped 0 rows", out.getvalue())
    
    def test_import_hotels_from_string_valid_data(self):
        # Create a city to link the hotels to
        city = City.objects.create(code='AMS', name='Amsterdam')
        
        csv_data = "AMS;AMS01;Hotel A\nAMS;AMS02;Hotel B\n"
        out = StringIO()
        
        command = Command()
        command.stdout = out
        command.import_hotels_from_string(csv_data)
        
        self.assertEqual(Hotel.objects.count(), 2)
        self.assertIn("Imported 2 hotels, skipped 0 rows", out.getvalue())
        
    def test_import_cities_from_string_invalid_data(self):
        csv_data = "AMS;Amsterdam\nBCN\n"
        out = StringIO()
        
        command = Command()
        command.stdout = out
        command.import_cities_from_string(csv_data)
        
        self.assertEqual(City.objects.count(), 1)
        self.assertIn("Imported 1 cities, skipped 1 rows", out.getvalue())
        
    def test_import_hotels_from_string_invalid_data(self):
        # Create a city to link the hotels to
        city = City.objects.create(code='AMS', name='Amsterdam')
        
        csv_data = "AMS;AMS01;Hotel A\nAMS;AMS02\n"
        out = StringIO()
        
        command = Command()
        command.stdout = out
        command.import_hotels_from_string(csv_data)
        
        self.assertEqual(Hotel.objects.count(), 1)
        self.assertIn("Imported 1 hotels, skipped 1 rows", out.getvalue())
        
    def test_import_hotels_from_string_missing_city(self):
        """
        Test that a hotel row referencing a non-existent city is skipped.
        """
        csv_data = "NONEXIST;AMS01;Hotel A\n"
        out = StringIO()

        command = Command()
        command.stdout = out
        command.import_hotels_from_string(csv_data)

        self.assertEqual(Hotel.objects.count(), 0)
        self.assertIn("City NONEXIST not found", out.getvalue())
        self.assertIn("skipped 1 rows", out.getvalue())
        
    def test_duplicate_cities(self):
        """
        Test that duplicate city entries are not created.
        """
        csv_data = "AMS;Amsterdam\nAMS;Amsterdam\n"
        out = StringIO()

        command = Command()
        command.stdout = out
        command.import_cities_from_string(csv_data)

        # Only one city should be imported.
        self.assertEqual(City.objects.count(), 1)
        self.assertIn("Row 2: City code AMS already exists", out.getvalue())


    def test_import_cities_from_file(self):
        csv_data = "AMS;Amsterdam\nBCN;Barcelona\n"
        # Create and write to temp file, then close it so that it is not locked.
        with NamedTemporaryFile('w+', delete=False) as temp_file:
            temp_file.write(csv_data)
            temp_file.flush()
            temp_file_name = temp_file.name  # Store file name.

        out = StringIO()
        call_command(
            'import_csv',
            mode='file',
            city_path=temp_file_name,
            hotel_path="",
            stdout=out
        )

        # After the command finishes, we expect 2 cities.
        self.assertEqual(City.objects.count(), 2)
        self.assertIn("Imported 2 cities", out.getvalue())

        # Remove the temporary file.
        os.unlink(temp_file_name)

    def test_import_hotels_from_file(self):
        # Create a city first so the hotel import can succeed.
        City.objects.create(code='AMS', name='Amsterdam')
        csv_data = "AMS;AMS01;Hotel A\nAMS;AMS02;Hotel B\n"
        with NamedTemporaryFile('w+', delete=False) as temp_file:
            temp_file.write(csv_data)
            temp_file.flush()
            temp_file_name = temp_file.name

        out = StringIO()
        call_command(
            'import_csv',
            mode='file',
            city_path="",
            hotel_path=temp_file_name,
            stdout=out
        )

        # Expect two hotels after command completes.
        self.assertEqual(Hotel.objects.count(), 2)
        self.assertIn("Imported 2 hotels", out.getvalue())

        os.unlink(temp_file_name)

    # --- Tests for HTTP-based import ---

    @patch("hotels.management.commands.import_csv.requests.get")
    def test_import_cities_from_http(self, mock_get):
        # Prepare fake CSV content for cities.
        csv_data = "AMS;Amsterdam\nBCN;Barcelona\n"
        fake_response = type("FakeResponse", (), {
            "content": csv_data.encode("utf-8"),
            "raise_for_status": lambda self: None
        })()
        mock_get.return_value = fake_response

        out = StringIO()
        command = Command()
        command.stdout = out
        command.import_cities_from_url("http://example.com/city.csv", auth=("python-demo", "claw30_bumps"))

        self.assertEqual(City.objects.count(), 2)
        self.assertIn("Imported 2 cities", out.getvalue())

    @patch("hotels.management.commands.import_csv.requests.get")
    def test_import_hotels_from_http(self, mock_get):
        # Create the referenced city.
        City.objects.create(code='AMS', name='Amsterdam')

        csv_data = "AMS;AMS01;Hotel A\nAMS;AMS02;Hotel B\n"
        fake_response = type("FakeResponse", (), {
            "content": csv_data.encode("utf-8"),
            "raise_for_status": lambda self: None
        })()
        mock_get.return_value = fake_response

        out = StringIO()
        command = Command()
        command.stdout = out
        command.import_hotels_from_url("http://example.com/hotel.csv", auth=("python-demo", "claw30_bumps"))

        self.assertEqual(Hotel.objects.count(), 2)
        self.assertIn("Imported 2 hotels", out.getvalue())