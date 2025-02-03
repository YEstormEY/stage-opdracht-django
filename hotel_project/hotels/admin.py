from django import forms
from django.contrib import admin
from django.shortcuts import render
from .models import City, Hotel
from django.urls import path

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')  # Fields to display in the list view
    search_fields = ('name', 'code')  # Fields to enable searching
    ordering = ('name',)  # Default ordering
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls

    def upload_csv(self, request):
        # Handle file upload for Cities
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            if csv_file is None:
                return render(request, 'admin/csv_upload.html', {"error": "No file uploaded"})
            
            try:  
                file_data = csv_file.read().decode("utf-8")
            except Exception as e:
                return render(request, 'admin/csv_upload.html', {"error": f"Error reading file: {e}"})
            
            csv_data = file_data.split("\n")
            skipped_rows = 0
            successfull_imports = 0
            

            # CSV file iteration
            for x in csv_data:
                if x:
                    fields = x.split(";")
                    if len(fields) != 2:
                        skipped_rows += 1
                        continue
                    
                    created = City.objects.get_or_create(
                        code=fields[0],
                        name=fields[1]
                    )
                    
                    if created:
                        successfull_imports += 1
            self.message_user(request, f"{successfull_imports} cities imported successfully. {skipped_rows} rows skipped.", level="success")

        # Render the form
        form = CsvImportForm()
        data = {"form": form, "table_name": "City"}
        return render(request, 'admin/csv_upload.html', data)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city')  # Fields to display in the list view
    list_filter = ('city',)  # Filter hotels by city
    search_fields = ('name', 'code')  # Fields to enable searching
    ordering = ('city', 'name')  # Default ordering
    
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('upload-csv/', self.upload_csv),]
        return new_urls + urls
    
    def upload_csv(self, request):
        # Handle file upload
        if request.method == "POST":
            csv_file = request.FILES["csv_upload"]
            if csv_file is None:
                return render(request, 'admin/csv_upload.html', {"error": "No file uploaded"})
            
            try:
                file_data = csv_file.read().decode("utf-8")
            except Exception as e:
                return render(request, 'admin/csv_upload.html', {"error": f"Error reading file: {e}"})
                
            
                
            csv_data = file_data.split("\n")
            skipped_rows = 0
            successfull_imports = 0
                
            for x in csv_data:
                if x:
                    fields = x.split(";")
                    
                    if len(fields) != 3:
                        skipped_rows += 1
                        continue
                    
                    try: 
                        city = City.objects.get(code=fields[0])
                    except City.DoesNotExist:
                        skipped_rows += 1
                        continue
                    
                    created = Hotel.objects.get_or_create(
                        code=fields[1],
                        name=fields[2],
                        city = City.objects.get(code=fields[0])
                    )
                    
                    if created:
                        successfull_imports += 1
                        
            self.message_user(request, f"{successfull_imports} hotels imported successfully. {skipped_rows} rows skipped.", level="success")

    
        form = CsvImportForm()
        data = {"form": form}
        return render(request, 'admin/csv_upload.html', data)
    
class CsvImportForm(forms.Form):
    
    csv_upload = forms.FileField()
