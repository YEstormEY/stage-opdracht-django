"""
Module: admin

This module defines Django admin classes that extend the functionality of the City and Hotel models by adding the ability to upload data from CSV files.

CSV File Formats:
    - City: CITY_CODE;NAME
    - Hotel: CITY_CODE;HOTEL_CODE;NAME
    
Error messages and import status are reported through Django's messages framework.

Classes:
    - CsvImportForm: Form class for CSV file upload.
    - CityAdmin: Admin class for the City model.
    - HotelAdmin: Admin class for the Hotel model.
"""

from django import forms
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from .models import City, Hotel
from django.urls import path

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """
    Admin configuration for the City model.
    
    This class provides:
        - A list display of city code and name
        - Search functionality by name and code
        - A custom URL for uploading CSV files to import cities
        
    The CSV upload method validates input data, handles errors gracefully, and displays
    feedback to the user.
    """
    list_display = ('code', 'name')  # Fields to display in the list view
    search_fields = ('name', 'code')  # Fields to enable searching
    ordering = ('name',)  # Default ordering
    
    def get_urls(self):
        """
        Extend default admin URLs with a URL for CSV uploads.

        Returns:
            list: A list of URL patterns including the CSV upload endpoint.
        """
        urls = super().get_urls()
        new_urls = [
            path(
                'upload-csv/',
                self.admin_site.admin_view(self.upload_csv),
                name='hotels_city_upload_csv'
            ),
        ]
        return new_urls + urls

    # Handles the CSV file upload
    def upload_csv(self, request):
        """
        Handles the CSV file uploads for the city model.
        
        When a POST request is made with a file under the field "csv_upload",
        the file is read and each line is split by semicolons. The format required is:
            CITY_CODE;NAME
            
        Rows not meeting the criteria(invalid format, missing values, duplicate city code) are skipped.
        The number of imported and skipped rows are reported back to the user.
        
        args:
            request: HttpRequest object containing the file upload
            
        Returns:
            HttpResponse: A rendered template with a CSV import form and help text.
        """
        if request.method == "POST":
            csv_file = request.FILES.get("csv_upload")
            
            # Check if a file was uploaded
            if not csv_file:
                messages.error(request, "No CSV file uploaded")
                return redirect("..")
            
            try:
                file_data = csv_file.read().decode("utf-8").strip()
                # Check if the file is empty
                if not file_data:
                    messages.error(request, "Uploaded file is empty")
                    return redirect("..")
                    
                csv_data = file_data.split("\n")
                row_errors = []
                imported_count = 0
                skipped_count = 0

                for idx, row in enumerate(csv_data, start=1):
                    row = row.strip()
                    # Skip empty rows
                    if not row:
                        continue
                        
                    try:
                        fields = row.split(";")
                        # Check for correct number of columns
                        if len(fields) != 2:
                            raise ValueError(f"Row {idx}: Expected 2 columns, found {len(fields)}")
                            
                        code, name = fields
                        if not code or not name:
                            raise ValueError(f"Row {idx}: Missing required values")
                            
                        # Check for existing city code
                        if City.objects.filter(code=code).exists():
                            raise ValueError(f"Row {idx}: City code {code} already exists")
                            
                        City.objects.create(code=code, name=name)
                        imported_count += 1
                        
                    except Exception as e:
                        skipped_count += 1
                        row_errors.append(f"- Row {idx}: {str(e)}")

                status_message = [
                    f"Successfully imported {imported_count} cities",
                    f"Skipped {skipped_count} rows due to errors:"
                ] + row_errors
                
                if row_errors:
                    messages.warning(request, "\n".join(status_message))
                else:
                    messages.success(request, status_message[0])

            except Exception as e:
                messages.error(request, f"Critical error processing file: {str(e)}")

        return render(request, 'admin/csv_upload.html', context={
            'form': CsvImportForm(),
            'help_text': "CSV format: CITY_CODE;NAME"
        })
    

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Hotel model.
    
    This class provides:
        - A list display of hotel code, name, and city
        - Filter functionality by city
        - Search functionality by name and code
        - A custom URL for uploading CSV files to import hotels
        
    During upload, the code checks that the associated city exists and that the hotel
    code is unique within that city.
    """
    list_display = ('code', 'name', 'city')  # Fields to display in the list view
    list_filter = ('city',)  # Filter hotels by city
    search_fields = ('name', 'code')  # Fields to enable searching
    ordering = ('city', 'name')  # Default ordering
    
    def get_urls(self):
        """
        Extend default admin URLs with a URL for hotel CSV uploads.

        Returns:
            list: A list of URL patterns including the CSV upload endpoint.
        """
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv, name='hotels_hotel_upload_csv',)]
        return new_urls + urls
    
    def upload_csv(self, request):
        """
        Handles the CSV file uploads for the hotel model.
        
        When a POST request is made with a file under the field "csv_upload", the file data is decoded and split into lines.
        Each line must have exactly 3 columns in the format:
            CITY_CODE;HOTEL_CODE;NAME
            
        The method verifies that the city exists and that the hotel code is unique for that city.
        Errors are recorded and communicated through the message framework.
        
        Args:
            request (HttpRequest): HttpRequest object containing the file upload
            
        Returns:
            HttpResponse: A rendered response with the upload form and instructions.
        """
        if request.method == "POST":
            csv_file = request.FILES.get("csv_upload")
            
            # Check if a file was uploaded
            if not csv_file:
                messages.error(request, "No CSV file uploaded")
                return redirect("..")

            try:
                file_data = csv_file.read().decode("utf-8").strip()
                row_errors = []
                imported_count = 0
                skipped_count = 0

                for idx, row in enumerate(file_data.split("\n"), start=1):
                    row = row.strip()
                    # Skip empty rows
                    if not row:
                        continue

                    try:
                        fields = row.split(";")
                        if len(fields) != 3:
                            raise ValueError("Expected 3 columns (City Code, Hotel Code, Name)")

                        city_code, hotel_code, name = fields
                        
                        city = City.objects.get(code=city_code)
                        
                        if not hotel_code or not name:
                            raise ValueError("Missing hotel code or name")
                            
                        if Hotel.objects.filter(code=hotel_code, city=city).exists():
                            raise ValueError("Hotel code already exists for this city")
                            
                        Hotel.objects.create(code=hotel_code, name=name, city=city)
                        imported_count +=1
                        
                    except City.DoesNotExist:
                        row_errors.append(f"- Row {idx}: City {city_code} not found")
                        skipped_count +=1
                    except Exception as e:
                        row_errors.append(f"- Row {idx}: {str(e)}")
                        skipped_count +=1

                status_message = [
                    f"Imported {imported_count} hotels",
                    f"Skipped {skipped_count} rows with errors:"
                ] + row_errors
                
                if row_errors:
                    messages.warning(request, "\n".join(status_message))
                else:
                    messages.success(request, status_message[0])

            except Exception as e:
                messages.error(request, f"File processing error: {str(e)}")

        return render(request, 'admin/csv_upload.html', context={
            'form': CsvImportForm(),
            'help_text': "CSV format: CITY_CODE;HOTEL_CODE;NAME"
        })
    
class CsvImportForm(forms.Form):
    """
    Form for CSV file uploads.

    This form provides a single file field named 'csv_upload'. The attached CSV file
    is processed by the respective Admin upload view (CityAdmin or HotelAdmin).
    """
    
    csv_upload = forms.FileField()
