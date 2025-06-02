# Appointment Booking System

A simple Django-based web application for booking and managing appointments.  
This project demonstrates user registration, authentication, role-based access, booking management, REST API, and basic logging.

---

## Features

- **User registration and login** (with role selection: Client or Provider)
- **Role-based navigation and permissions**
    - Clients can book and cancel appointments
    - Providers can create and manage their own timeslots
- **Account deletion**
- **Password reset via email (console backend)**
- **REST API** for bookings (with authentication)
- **Swagger/OpenAPI documentation**
- **Logging** (to console and file)
- **Basic CSS styling and responsive layout**

---

## Technologies

- Python 3.11+
- Django 5.x
- Django REST Framework
- drf-yasg (Swagger docs)
- SQLite (default, easy to switch)
- Bootstrap/CSS for styling

---

## Setup & Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/endrelazar/Appointment_api.git
    cd your-repo
    ```

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser (optional, for admin)**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server**
    ```bash
    python manage.py runserver
    ```

7. **Access the app**
    - Web: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
    - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
    - Swagger API docs: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## REST API

- **Authentication required** for all endpoints.
- Example endpoint:  
    - `POST /api/bookings/` – Create a new booking (as client)
    - `GET /api/bookings/` – List your bookings

See `/swagger/` for full interactive API documentation.

---

## Testing

Run all tests with:

```bash
python manage.py test
```

---


## License

MIT License

---

## Author

[Endre Lazar]  
