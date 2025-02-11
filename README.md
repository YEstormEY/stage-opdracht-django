# Hotel Management System for Django

This project is a Django-based hotel and city management system. It provides functionality to manage cities and hotels, import data via CSV files using both HTTP and local file modes, and render city and hotel listings through views and templates.

## Table of Contents



## Overview

This Django project provides core functionalities to manage cities and hotels.

Key components include:
- **Models**: City and Hotel models to store city and hotel data.
- **Views**: City and Hotel views to render city and hotel listings.
- **Templates**: City and Hotel templates to render city and hotel listings.
- **Management Commands**: Import city and hotel data via CSV files using both HTTP and local file modes.
- **Admin**: Admin interface to manage city and hotel data.


## Features

- **CSV Data Import:** 
  - Supports importing cities and hotels with specific CSV formats.
  - Two modes available: `http` (fetch from URL) and `file` (local file upload).
- **Dynamic Listings:** 
  - Views to render a list of cities.
  - Views to render a list of hotels, with an option to filter hotels by a selected city.
- **User-Friendly Templates:** 
  - HTML templates for displaying city selection and hotel listings.


## Installation and Setup

1. **Clone the Repository:**
    ```
    git clone https://example.com/your-repo.git
    cd your-repo
    ```

2. **Create a Virtual Environment and Install Dependencies:**

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure the Django Project:**

   - Update the project's settings in `settings.py` as per your environment.
   - Ensure the `hotels` application is added to the `INSTALLED_APPS` list.

4. **Apply Migrations:**

   ```
   python manage.py migrate
   ```

5. **Create a Superuser for the Admin Interface**
    ```bash
    python manage.py createsuperuser
    ```

## Project Structure
```
hotel_project/
├── hotels/
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── import_csv.py
│   ├── tests/
│   │   ├── test_import_csv.py
│   │   └── test_admin.py
│   ├── models.py
│   ├── views.py
│   └── admin.py
├── templates/
│   │   ├── hotels/
│   │   │   ├── city_list.html
│   │   │   └── hotel_list.html
│   │   └── admin/
│   │       ├── city/
│   │       │   └── change_list.html
│   │       ├── hotel/
│   │       │   └── change_list.html
│   │       └── csv_upload.html
├── manage.py
└── requirements.txt
```

### Explanation of Key Components

- **`models.py`**: 
  Defines the `City` and `Hotel` models for the database.

- **`views.py`**: 
  Contains views like `CityView`, `HotelView`, and `HotelInCityView` to handle requests and render data.

- **`admin.py`**: 
  Extends Django's admin interface for managing cities and hotels.

- **`import_csv.py`**: 
  A custom management command to import City and Hotel data from a CSV file or authenticated HTTP source.

- **Templates**:
  - `city_list.html`: Displays available cities for selection.
  - `hotel_list.html`: Displays a list of hotels for the selected city.
  - `csv_upload.html`: Admin interface for importing CSV files into the database.


## Usage

### Management Commands
This project includes a custom management command for importing city and hotel data into the database.

#### Command Usage
To run the command, use the following syntax:

- **Import via HTTP**:
    ```bash
    python manage.py import_csv --mode=http \
        --city-url="http://example.com/city.csv" \
        --hotel-url="http://example.com/hotel.csv"
    ```

- **Import from Local Files**:
    ```bash
    python manage.py import_csv --mode=file \
        --city-path="/path/to/city.csv" \
        --hotel-path="/path/to/hotel.csv"
    ```

#### CSV Format
The expected CSV file format is as follows:

- **City CSV**:
    ```
    CITY_CODE;NAME
    ```
- **Hotel CSV**:
    ```
    CITY_CODE;HOTEL_CODE;NAME
    ```

### Templates
- **`city_list.html`**:
  Display cities in a dropdown for selection and submission.
- **`hotel_list.html`**: 
  Displays the list of hotels filtered by the selected city.


### Admin Functionality

Django’s admin interface, accessible at [/admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/), is tailored for efficient management of city and hotel data. The system features:

- **City Management:**  
  Admins can view and manage cities via the `admin/city/change_list.html` template, which supports search and bulk operations.

- **Hotel Management:**  
  Hotels are managed through the `admin/hotel/change_list.html` template, offering filtering by city and straightforward edits.

- **CSV Upload:**  
  The `admin/csv_upload.html` template enables direct CSV file uploads from the admin interface, streamlining data import with built-in error reporting using Django's messages framework. 

## Running Tests

This project includes a suite of unit tests to ensure the correct functionality of the CSV import logic and the views.

### To run the tests:

1. Activate your virtual environment and install dependencies:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run the Django test runner:
   ```bash
   python manage.py test
   ```

3. (Optional) To view test coverage, you can run:
   ```bash
   coverage run --source=. manage.py test
   coverage report
   ```

