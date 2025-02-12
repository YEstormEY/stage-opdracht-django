# Hotel Management System for Django

This project is a Django-based hotel and city management system. It allows for managing cities and hotels, importing data via CSV files (using HTTP and local file modes), and rendering listings through views and templates. A React frontend provides a user-friendly interface for interacting with the system.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Management Commands](#management-commands)
  - [Frontend Interaction](#frontend-interaction)
  - [Admin Functionality](#admin-functionality)
- [Running Tests](#running-tests)

## Overview

This Django project provides core functionalities to manage cities and hotels.

Key components include:

- **Models**: City and Hotel models to store city and hotel data.
- **Views**: RESTful city and hotel views to render city and hotel data.
- **Templates**: City and hotel templates for listing and data display.
- **Management Commands**: Import city and hotel data via CSV files using both HTTP and local file modes.
- **Admin**: Admin interface to manage city and hotel data.
- **React Frontend**: A single-page application for end-user interaction.

## Features

- **CSV Data Import:**
  - Supports importing cities and hotels with specific CSV formats.
  - Two modes available: `http` (fetch from URL) and `file` (local file upload).

- **Dynamic Listings:**
  - Views to render a list of cities.
  - Views to render a list of hotels, with an option to filter hotels by a selected city.

- **User-Friendly Frontend (React):**
  - City search supported by an autocomplete feature.
  - Dynamic filtering of hotels based on city selection.

- **Admin Functionality:**
  - Full CRUD operations for city and hotel data.
  - CSV upload capability via the admin dashboard.

## Installation and Setup

Follow these steps to set up the backend and frontend:

### Backend (Django)

1. **Clone the Repository:**
   ```bash
   git clone https://example.com/your-repo.git
   cd your-repo
   ```

2. **Create a Virtual Environment and Install Dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure the Django Project:**
   - Update the project's settings in `settings.py` as per your environment.
   - Ensure the `hotels` application is added to the `INSTALLED_APPS` list.

4. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser for the Admin Interface**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Backend Server**:
   ```bash
   python manage.py runserver
   ```

### Frontend (React)

1. **Navigate to the Frontend Directory:**
   ```bash
   cd hotel-frontend
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Start the Frontend Development Server:**
   ```bash
   npm start
   ```

   The React application can be accessed at `http://localhost:3000`. Ensure the backend (Django) is running at the same time to provide the required APIs.

---

## Project Structure

```
hotel_project/
├── hotel_project/           # Django backend core settings and configurations
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── hotels/                  # Django app managing hotels and cities
│   ├── migrations/
│   ├── management/
│   │   └── commands/
│   │       └── import_csv.py
│   ├── tests/
│   │   ├── test_import_csv.py
│   │   └── test_admin.py
│   ├── models.py
│   ├── views.py
│   ├── api_views.py
│   ├── serializers.py
│   └── ..
├── templates/               # Django templates
│   ├── admin/
│   │   ├── hotels/
│   │   │   ├── city/
│   │   │   │   ├── change_list.html
│   │   │   └── hotel/
│   │   │       ├── change_list.html
│   │   └── csv_upload.html
├── static/                  # Django static files
│   ├── css/
│   ├── js/
│   └── ...
├── manage.py
├── db.sqlite3               # Database for development
└── hotel-frontend/          # React frontend
    ├── package.json
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── App.js           # Core React app
    │   ├── components/
    │   │   ├── CitySelectPage.js
    │   │   └── HotelsPage.js
    │   ├── styles/
    │   │   └── styles.css
    │   └── tests/
    │       ├── CitySelectPage.test.js
    │       └── HotelsPage.test.js
    └── ...
```

---

## Usage

### Management Commands

This project includes a custom Django management command for importing city and hotel data into the database.

#### Command Usage

- **Import via HTTP:**
  ```bash
  python manage.py import_csv --mode=http \
      --city-url="http://example.com/city.csv" \
      --hotel-url="http://example.com/hotel.csv"
  ```

- **Import from Local Files:**
  ```bash
  python manage.py import_csv --mode=file \
      --city-path="/path/to/city.csv" \
      --hotel-path="/path/to/hotel.csv"
  ```

#### CSV Format

- **City CSV:**
  ```
  CITY_CODE;NAME
  ```
- **Hotel CSV:**
  ```
  CITY_CODE;HOTEL_CODE;NAME
  ```

---

### Frontend Interaction

1. **City Selection:**
   - Use the React app to select a city from the provided list or search using the autocomplete feature.
2. **View Hotels:**
   - Once a city is selected, view a list of hotels specific to that city.
3. **Error Handling:**
   - Friendly error messages in case of API request failures ensure a smooth user experience.

---

### Admin Functionality

Django’s admin interface (accessible at `/admin`) supports:

- **City Management**: Add, edit, or delete cities.
- **Hotel Management**: Manage hotels and link them to cities.
- **CSV Upload**: Upload CSV files for automated data import.
- **Error Reporting**: Built-in feedback for errors during data import.

---

## Running Tests

This project includes a suite of unit tests for both the Django backend and React frontend:

### Backend (Django)
1. Activate your virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Run the Django test runner:
   ```bash
   python manage.py test
   ```
3. (Optional) View test coverage:
   ```bash
   coverage run --source=. manage.py test
   coverage report
   ```

### Frontend (React)
1. Navigate to the frontend directory:
   ```bash
   cd hotel-frontend
   ```
2. Run the test suite:
   ```bash
   npm test
   ```