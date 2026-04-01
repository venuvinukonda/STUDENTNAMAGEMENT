# Student Management System

A comprehensive web-based student management system built with Django (Backend), HTML, Tailwind CSS, and JavaScript (Frontend) designed for colleges to track student progress and manage academic records.

## Features

### Core Functionality
- **Student Management**: Add, edit, delete, and view student profiles with comprehensive information
- **Course Management**: Manage courses with credit hours and descriptions
- **Program Management**: Define degree programs and their duration
- **Enrollment Management**: Enroll students in courses and track enrollment status
- **Grade Management**: Record and track attendance, midterm, final, and assignment scores
- **Progress Tracking**: Monitor student academic progress and performance metrics
- **Reporting**: Generate analytics and performance reports

### Student Tracking Capabilities
- GPA calculation and tracking
- Attendance monitoring
- Academic warning system for low performers
- Performance history by semester
- Progress visualization

### Integrated Features
- Search and filter functionality
- Pagination for large datasets
- Form validation (client and server-side)
- Responsive design for mobile and desktop
- Admin dashboard for system management
- Database indexing for optimal performance

## Technology Stack

### Backend
- **Framework**: Django 5.1.5
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Python**: 3.8+

### Frontend
- **HTML5**: Semantic markup
- **CSS**: Tailwind CSS with custom styling
- **JavaScript**: Vanilla JS for interactivity
- **Charts**: Chart.js for data visualization

## Project Structure

```
SNAPSERVICE/
├── SNAPSERVICE/              # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── students/                 # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── tests.py             # Test cases
│   └── templates/students/  # HTML templates
├── static/                   # Static files
│   ├── css/custom.css       # Custom styling
│   └── js/main.js           # JavaScript functionality
├── templates/               # Project templates
│   └── base.html            # Base template
├── manage.py                # Django management
└── requirements.txt         # Python dependencies
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Clone/Extract the project**
   ```bash
   cd SNAPSERVICE
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   # Follow prompts to create admin user
   ```

6. **Collect static files** (for production)
   ```bash
   python manage.py collectstatic --noinput
   ```

## Running the Application

### Development Server

```bash
python manage.py runserver
```

The application will be accessible at: `http://127.0.0.1:8000/`

### Access the Admin Panel

Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

## Usage Guide

### Dashboard
- Main overview page showing key statistics
- Quick action buttons for common tasks
- Navigation to different modules

### Students Module
1. **View Students**: `Students` menu → Click on student name for details
2. **Add Student**: Click `+ Add Student` button
3. **Edit Student**: Click `Edit` on student list
4. **Delete Student**: Click `Delete` (confirmation required)

### Courses Module
1. **View Courses**: `Courses` menu
2. **Add Course**: Click `+ Add Course`
3. **Edit/Delete**: Similar to students

### Enrollments Module
1. **Enroll Student**: Click `+ Add Enrollment`
2. **Track Enrollments**: View list with status and grades
3. **Update Grades**: Click `Grades` button in enrollment list

### Grades Management
- Record attendance (0-100%)
- Enter midterm score (0-100)
- Enter final exam score (0-100)
- Enter assignment score (0-100)
- System automatically calculates total and grade

Grade Calculation:
- Midterm: 30%
- Final Exam: 50%
- Assignments: 15%
- Attendance: 5%

Grade Scale:
- A: 90-100
- B: 80-89
- C: 70-79
- D: 60-69
- F: Below 60

### Reports
- Top 10 performing students
- Students on academic warning (GPA < 2.0)
- Enrollment statistics

## Database Models

### Student
- Roll Number (Unique)
- Personal Information (Name, Email, DOB, etc.)
- Academic Information (Program, Semester, GPA)
- Address Information
- Guardian Contact Information
- Timestamps

### Course
- Course Code (Unique)
- Name
- Credit Hours
- Description
- Creation Date

### Program
- Name
- Code (Unique)
- Duration (Years)

### Enrollment
- Student & Course (Foreign Keys)
- Semester & Year
- Status (Enrolled, Completed, Dropped, Failed)
- Scores (Midterm, Final, Assignment, Attendance)
- Automatic GPA Calculation
- Letter Grade Assignment

### Progress
- Student Progress Record
- Semester & Year
- Cumulative & Semester GPA
- Courses Passed/Failed
- Academic Warning Status
- Attendance Tracking

## Features Explained

### Grade Calculation
Automatic weighted calculation based on:
- Class participation & attendance
- Midterm examination
- Final examination
- Assignments and projects

### GPA Tracking
- Semester GPA calculation
- Cumulative GPA tracking
- Academic warning system (GPA < 2.0)
- Progress history per student

### Search & Filter
- Search by roll number, name, or email
- Filter by status, semester, or program
- Real-time filtering with pagination

### Responsive Design
- Mobile-friendly interface
- Tablet and desktop optimized
- Touch-friendly navigation

## Admin Panel Features

- Student management
- Course and program administration
- Enrollment oversight
- Progress monitoring
- Bulk operations support

## Testing

Run tests with the following command:

```bash
python manage.py test students
```

### Sample Test Cases Included
- Student creation and retrieval
- Email uniqueness validation
- Grade calculation
- Enrollment status tracking

## Deployment

### For Production:

1. **Update Settings**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Use PostgreSQL**
   ```bash
   pip install psycopg2-binary
   ```

3. **Set Environment Variables**
   - Django Secret Key
   - Database credentials
   - Allowed hosts

4. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

5. **Use Gunicorn or similar**
   ```bash
   pip install gunicorn
   gunicorn SNAPSERVICE.wsgi:application
   ```

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Migration Issues
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

## Future Enhancements

- Email notifications for academic warnings
- PDF report generation
- Student login portal
- Parent access portal
- Advanced analytics dashboard
- Automated backup system
- API for mobile application
- Multi-language support
- Attendance via QR code

## Security Considerations

- CSRF protection enabled
- SQL injection prevention through ORM
- XSS protection (Tailwind)
- User authentication required
- Form validation (client and server)
- Secure password storage

## Support & Documentation

For issues or questions:
1. Check the Django documentation: https://docs.djangoproject.com/
2. Review Tailwind CSS documentation: https://tailwindcss.com/docs
3. Check template syntax: https://docs.djangoproject.com/en/stable/topics/templates/

## License

This project is designed for educational purposes at colleges and universities.

## Contributors

- Initial Development: SNAPSERVICE Team

---

**Last Updated**: 2024
**Version**: 1.0.0

Happy Learning! 🎓
