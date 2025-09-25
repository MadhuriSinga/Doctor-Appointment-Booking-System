# DocBook - Doctor Appointment Booking System

A comprehensive Django-based web application for managing doctor appointments, patient records, and medical history.

## Features


#### Patient Features
- **User Registration & Authentication**: Secure patient and doctor registration with email verification
- **Doctor Search & Filtering**: Advanced search by specialty, location, experience, and consultation fee
- **Appointment Booking**: Easy appointment scheduling with time slot validation
- **Appointment Management**: View, filter, and cancel appointments
- **Medical History**: Complete medical records and history tracking
- **Profile Management**: Comprehensive patient profile with medical information
- **Dashboard**: Personalized dashboard with appointment statistics

#### Doctor Features
- **Professional Profile**: Detailed doctor profiles with specialty, experience, and bio
- **Appointment Management**: View, accept, reject, and update appointments
- **Medical Records**: Create and manage patient medical records
- **Availability Management**: Set and manage weekly availability schedule
- **Patient History**: View patient medical history and previous appointments
- **Dashboard**: Professional dashboard with appointment statistics

#### System Features
- **Role-based Access Control**: Separate interfaces for patients and doctors
- **Email Notifications**: Automated email confirmations and reminders
- **Data Validation**: Comprehensive form validation and error handling
- **Responsive Design**: Mobile-friendly Bootstrap-based UI
- **Admin Interface**: Full Django admin integration
- **Database Management**: SQLite database with proper migrations

## Tech Stack

- **Backend**: Python 3.10+, Django 5.2.4
- **Frontend**: HTML5, CSS3, Bootstrap 5.1.3, JavaScript, jQuery
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Email**: Django email backend with SMTP support
- **Image Handling**: Pillow for profile pictures
- **Authentication**: Django's built-in authentication system

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd doctor_appointment
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   # On Windows
   env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Project Structure

```
doctor_appointment/
├── doctor_appointment/          # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                    # User authentication and profiles
│   ├── models.py               # CustomUser, DoctorProfile, PatientProfile
│   ├── views.py                # Registration, login, profile management
│   ├── forms.py                # User registration and profile forms
│   ├── admin.py                # Admin interface configuration
│   └── management/
│       └── commands/           # Custom management commands
├── appointments/               # Appointment management
│   ├── models.py              # Appointment, MedicalRecord, DoctorAvailability
│   ├── views.py               # Appointment CRUD, dashboards
│   ├── forms.py               # Appointment and medical record forms
│   └── admin.py               # Admin interface
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── home.html              # Homepage
│   ├── accounts/              # Authentication templates
│   └── appointments/          # Appointment templates
├── static/                    # Static files (CSS, JS, images)
├── media/                     # User uploaded files
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## Usage Guide

### For Patients

1. **Registration**
   - Visit the homepage and click "Register as Patient"
   - Fill in your details and verify your email
   - Complete your profile with medical information

2. **Finding Doctors**
   - Use the "Find Doctors" page to search for doctors
   - Filter by specialty, location, experience, or consultation fee
   - View doctor profiles and availability

3. **Booking Appointments**
   - Select a doctor and click "Book Appointment"
   - Choose date and time (within doctor's availability)
   - Add notes about your concerns
   - Receive email confirmation

4. **Managing Appointments**
   - View all appointments in your dashboard
   - Filter by status (Pending, Confirmed, Completed, Cancelled)
   - Cancel appointments if needed
   - View appointment details and medical records

### For Doctors

1. **Registration**
   - Visit the homepage and click "Register as Doctor"
   - Fill in professional details and specialty
   - Wait for admin approval (account will be activated)

2. **Profile Management**
   - Complete your professional profile
   - Set consultation fees and experience
   - Upload profile picture and bio
   - Manage your availability schedule

3. **Appointment Management**
   - View all appointments in your dashboard
   - Accept or reject pending appointments
   - Update appointment status and add notes
   - Create medical records after appointments

4. **Patient Care**
   - View patient medical history
   - Create detailed medical records
   - Prescribe medications and treatments
   - Schedule follow-up appointments

## Database Models

### User Models
- **CustomUser**: Extended user model with patient/doctor flags
- **DoctorProfile**: Doctor-specific information (specialty, location, fees)
- **PatientProfile**: Patient medical information and history

### Appointment Models
- **Appointment**: Core appointment data with status tracking
- **MedicalRecord**: Detailed medical records linked to appointments
- **DoctorAvailability**: Doctor's weekly schedule

## API Endpoints

### Authentication
- `POST /accounts/register/patient/` - Patient registration
- `POST /accounts/register/doctor/` - Doctor registration
- `GET /accounts/activate/<uidb64>/<token>/` - Email activation
- `GET /accounts/login/` - User login
- `GET /accounts/logout/` - User logout

### Appointments
- `GET /appointments/doctors/` - List all doctors with filtering
- `GET /appointments/doctors/<id>/` - Doctor details
- `POST /appointments/book/<doctor_id>/` - Book appointment
- `GET /appointments/patient/dashboard/` - Patient dashboard
- `GET /appointments/doctor/dashboard/` - Doctor dashboard
- `GET /appointments/appointment/<id>/` - Appointment details
- `POST /appointments/appointment/<id>/update/` - Update appointment
- `POST /appointments/appointment/<id>/cancel/` - Cancel appointment

### Medical Records
- `GET /appointments/patient/medical-history/` - Patient medical history
- `POST /appointments/appointment/<id>/medical-record/` - Create medical record

### Profiles
- `GET /appointments/patient/profile/` - Patient profile management
- `GET /appointments/doctor/profile/` - Doctor profile management
- `GET /appointments/doctor/availability/` - Manage availability

## Configuration

### Email Settings
Update `settings.py` for production email configuration:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@domain.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Database Settings
For production, update database settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'docbook_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Testing

Run the test suite:
```bash
python manage.py test
```

Test email functionality:
```bash
python manage.py send_test_email your-email@example.com
```

## Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up email backend
4. Configure static file serving
5. Set up media file serving
6. Configure security settings
7. Set up SSL/HTTPS
8. Configure logging

### Environment Variables
Create a `.env` file for sensitive settings:
```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-password
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Email: support@docbook.com
- Documentation: [Project Wiki]
- Issues: [GitHub Issues]

## Changelog

### Version 1.0.0
- Initial release
- Complete patient and doctor management
- Appointment booking and management
- Medical records system
- Email verification
- Responsive UI design
- Admin interface
- Comprehensive documentation

---

**DocBook** - Making healthcare accessible, one appointment at a time.




