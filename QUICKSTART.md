# Quick Start Guide - Student Management

## Getting Started in 5 Minutes

### 1. Setup Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_db  # Load sample data
```

### 4. Run Server
```bash
python manage.py runserver
```

### 5. Access Application
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Student List**: http://127.0.0.1:8000/students/
- **Dashboard**: http://127.0.0.1:8000/

## Key Features to Try

### Student Management
1. Go to **Students** menu
2. Click **+ Add Student** to create new student
3. Fill form and submit
4. View student details by clicking their name
5. Update/Delete from student list

### Course Management
1. Go to **Courses** menu
2. Click **+ Add Course**
3. Add course code, name, and credit hours

### Enrollment Process
1. Go to **Enrollments** menu
2. Click **+ Add Enrollment**
3. Select student and course
4. Set semester and year
5. Submit

### Grade Management
1. Go to **Grades** menu
2. Update attendance and scores
3. System automatically calculates grade
4. View calculated total score and letter grade

### View Reports
1. Go to **Reports** menu
2. See top performing students
3. View students on academic warning
4. Check enrollment statistics

## Admin Panel Usage

### Login
1. Visit http://127.0.0.1:8000/admin/
2. Enter superuser credentials
3. Browse all models and data

### Bulk Actions
- Select multiple records
- Use dropdown to apply actions
- Delete multiple records at once

## Sample Data

The `populate_db` command creates:
- 5 Programs (CS, BA, ME, CE, EC)
- 8 Courses
- 15 Students with enrollments

## Useful Commands

```bash
# Run tests
python manage.py test students

# Create superuser
python manage.py createsuperuser

# Populate sample data
python manage.py populate_db

# Clear database
python manage.py flush

# Check for issues
python manage.py check

# Run migrations
python manage.py makemigrations students
python manage.py migrate
```

## Troubleshooting

**Port 8000 already in use?**
```bash
python manage.py runserver 8001
```

**Database errors?**
```bash
python manage.py migrate --run-syncdb
```

**Need to start fresh?**
```bash
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

## Next Steps

1. Customize settings in `SNAPSERVICE/settings.py`
2. Add your college information in admin panel
3. Create additional courses and programs
4. Import student data
5. Configure email settings for notifications
6. Setup production environment

## File Locations

- **Templates**: `students/templates/students/`
- **Static Files**: `static/css/` and `static/js/`
- **Models**: `students/models.py`
- **Views**: `students/views.py`
- **URLs**: `students/urls.py`

## Support

For detailed information, see README.md
