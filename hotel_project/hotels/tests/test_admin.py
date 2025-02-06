"""
Module: test_admin

This module contains unit tests for the CSV upload functionality provided in the Django
admin for the City and Hotel models. It uses django's test framework to stimulate the file uploads,
check responses, and verify that the corresponding models are correctly updated.

The tests ensure that:
    - Valid CSV leads to the successful creation of City and Hotel instances.
    - CSV file including invalid or incomplete data are handled correctly.
    - Duplicate entries or missing cities are not created.
    
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from hotels.models import City, Hotel



class BaseAdminTestCase(TestCase):
    """
    Base test case for all admin tests.
    
    This class sets up a client and an admin user, ensuring every test has a logged in superuser. 
    It is used as a base for both city and hotel admin tests.
    """
    def setUp(self):
        """
        Set up the test client and create an admin user.
        """
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username='test',
            password='adminpass',
            email='admin@example.com'
        )
        self.client.login(username='test', password='adminpass')
        

class CityAdminTest(BaseAdminTestCase):
    """
    Test cases for the csv upload functionality for the City model.
    
    It verifies that:
        - A valid CSV file with city data is correctly uploaded.
        - CSV files with invalid or incomplete data are handled correctly.
    """
    
    def _upload_csv(self, data):
        """
        Helper method to upload a CSV file with city data.
        
        Constructs a SimpleUploadedFile object from the provided data and sends a POST request to the
        city upload url with the file.
        
        Args:
            data (str): The content of the CSV file.
            
        Returns:
            HttpResponse: The response from the upload request.
        """
        csv_file = SimpleUploadedFile(
            name='cities.csv',
            content=data.encode('utf-8'),
            content_type='text/csv'
        )
        return self.client.post(
            reverse('admin:hotels_city_upload_csv'),
            {'csv_upload': csv_file},
            follow=True
        )
        
    # Test cases
    # Test for successful upload of a CSV file with 2 cities    
    def test_upload_csv_success(self):
        """Test valid CSV upload with 2 cities"""
        response = self._upload_csv('MAD;Madrid\nDKR;Dakar\n')        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(City.objects.count(), 2)
        self.assertContains(response, "2 cities imported successfully. 0 rows skipped.")

    # Test for successful upload of a CSV file with 1 correct and 1 incorrect row
    def test_upload_csv_invalid_data(self):
        """Test CSV with 1 valid and 1 invalid row"""
        response = self._upload_csv('MAD;Madrid\nDKR\n')
        self.assertEqual(City.objects.count(), 1)
        self.assertContains(response, "1 cities imported successfully. 1 rows skipped.")
    
    # Test for empty CSV file
    def test_empty_csv(self):
        """Test empty CSV file"""
        response = self._upload_csv('')
        self.assertEqual(City.objects.count(), 0)
        self.assertContains(response, "No data in file")
        
    # Test for duplicate city code
    def test_duplicate_city_code(self):
        """Test duplicate city code"""
        # First upload
        self._upload_csv('MAD;Madrid\n') 
        # Second upload with duplicate city code.
        response = self._upload_csv('MAD;Madrid\n')

        # Verify that only one city exists.
        self.assertEqual(City.objects.count(), 1)
        city = City.objects.get(code='MAD')
        self.assertEqual(city.name, 'Madrid')

        # Retrieve messages from the response's request.
        message_list = list(get_messages(response.wsgi_request))
        # Expecting one message.
        self.assertEqual(len(message_list), 1)

        # Verify the message level indicates success.
        self.assertEqual(message_list[0].level, messages.SUCCESS)

        self.assertIn("1 cities imported successfully. 0 rows skipped", message_list[0].message)
        
# This testcase tests the csv upload functionality for the Hotel model
class HotelAdminTest(BaseAdminTestCase):
    """
    Test cases for the csv upload functionality for the Hotel model.
    
    It verifies that:
        - A valid CSV file with hotel data is correctly uploaded.
        - CSV files with invalid or incomplete data are handled correctly.
    """
    
    # Helper function to upload a CSV file(city data)
    def _upload_city_csv(self, data):
        """
        Helper method to upload a CSV file with city data. Is used to create cities before hotels.
        
        Constructs a SimpleUploadedFile object from the provided data and sends a POST request to the
        city upload url with the file.
        
        Args:
            data (str): The content of the CSV file.
            
        Returns:
            HttpResponse: The response from the upload request.
        """
        csv_file = SimpleUploadedFile(
            name='cities.csv',
            content=data.encode('utf-8'),
            content_type='text/csv'
        )
        return self.client.post(
            reverse('admin:hotels_city_upload_csv'),
            {'csv_upload': csv_file},
            follow=True
        )
    
    # Helper function to upload a CSV file(hotel data)
    def _upload_csv(self, data):
        """
        Helper method to upload a CSV file with hotel data.
        
        Constructs a SimpleUploadedFile object from the provided data and sends a POST request to the
        hotel upload url with the file.
        
        Args:
            data (str): The content of the CSV file.
        
        Returns:
            HttpResponse: The response from the upload request.
        """
        csv_file = SimpleUploadedFile(
            name='hotels.csv',
            content=data.encode('utf-8'),
            content_type='text/csv'
        )
        return self.client.post(
            reverse('admin:hotels_hotel_upload_csv'),
            {'csv_upload': csv_file},
            follow=True
        )
    
    # Test cases
    # Test for successful upload of a CSV file with 2 hotels
    def test_upload_csv_success(self):
        """Test valid CSV upload with 2 hotels"""
        # create 2 cities
        self._upload_city_csv('ANT;Antwerpen\nAMS;Amsterdam\n')
        response = self._upload_csv('ANT;ANT03;Test Plaze\nAMS;AMS66;De amsterdammer\n')        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Hotel.objects.count(), 2)
        self.assertContains(response, "2 hotels imported successfully. 0 rows skipped.")
        
    # Test for successful upload of a CSV file with 1 correct and 1 incorrect row
    def test_upload_csv_invalid_data(self):
        """Test CSV with 1 valid and 1 invalid row"""
        self._upload_city_csv('ANT;Antwerpen\n')
        response = self._upload_csv('ANT;ANT03;Test Plaze\nAMS;AMS66\n')
        self.assertEqual(Hotel.objects.count(), 1)
        self.assertContains(response, "1 hotels imported successfully. 1 rows skipped.")
        
    # Test for missing city
    def test_upload_with_missing_city(self):
        """Test CSV with missing city"""
        self._upload_city_csv('ANT;Antwerpen\n')
        response = self._upload_csv('AMS;AMS03;Test Plaza\n')
        self.assertEqual(Hotel.objects.count(), 0)
        self.assertContains(response, "0 hotels imported successfully. 1 rows skipped.")
        
    # Test for empty CSV file
    def test_empty_csv(self):
        """Test empty CSV file"""
        response = self._upload_csv('')
        self.assertEqual(Hotel.objects.count(), 0)
        self.assertContains(response, "No data in file")
        

        
        