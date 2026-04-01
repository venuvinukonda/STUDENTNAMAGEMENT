from django.core.management.base import BaseCommand
from django.utils import timezone
from students.models import Student, Course, Program, Enrollment, Progress
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data for testing'

    def handle(self, *args, **options):
        """Create sample data"""
        self.stdout.write('Creating sample data...')

        # Create Programs
        programs = []
        program_data = [
            {'name': 'Computer Science', 'code': 'CS', 'duration': 4},
            {'name': 'Business Administration', 'code': 'BA', 'duration': 4},
            {'name': 'Mechanical Engineering', 'code': 'ME', 'duration': 4},
            {'name': 'Civil Engineering', 'code': 'CE', 'duration': 4},
            {'name': 'Electronics Engineering', 'code': 'EC', 'duration': 4},
        ]

        for prog in program_data:
            p, created = Program.objects.get_or_create(
                code=prog['code'],
                defaults={
                    'name': prog['name'],
                    'duration_years': prog['duration']
                }
            )
            programs.append(p)
            if created:
                self.stdout.write(f"Created program: {p.name}")

        # Create Courses
        courses = []
        course_data = [
            {'name': 'Introduction to Python', 'code': 'CS101', 'credits': 3},
            {'name': 'Data Structures', 'code': 'CS102', 'credits': 3},
            {'name': 'Web Development', 'code': 'CS201', 'credits': 4},
            {'name': 'Database Management', 'code': 'CS202', 'credits': 3},
            {'name': 'Business Economics', 'code': 'BA101', 'credits': 3},
            {'name': 'Financial Accounting', 'code': 'BA102', 'credits': 4},
            {'name': 'Engineering Mechanics', 'code': 'ME101', 'credits': 4},
            {'name': 'Thermodynamics', 'code': 'ME102', 'credits': 4},
        ]

        for course in course_data:
            c, created = Course.objects.get_or_create(
                code=course['code'],
                defaults={
                    'name': course['name'],
                    'credit_hours': course['credits']
                }
            )
            courses.append(c)
            if created:
                self.stdout.write(f"Created course: {c.name}")

        # Create Students
        first_names = ['John', 'Jane', 'Michael', 'Emma', 'David', 'Sarah', 'James', 'Lisa', 'Robert', 'Mary']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        semesters = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th']

        students_created = 0
        for i in range(1, 16):  # Create 15 students
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            roll_number = f"CS{1000+i}"
            program = random.choice(programs)
            semester = random.choice(semesters[:4])  # First 4 semesters
            gpa = round(random.uniform(1.5, 4.0), 2)

            student, created = Student.objects.get_or_create(
                roll_number=roll_number,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': f"{first_name.lower()}.{last_name.lower()}{i}@university.edu",
                    'phone': f"555-{1000+i}",
                    'date_of_birth': date(2000+random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                    'gender': random.choice(['M', 'F']),
                    'program': program,
                    'semester': semester,
                    'status': 'active',
                    'admission_date': date(2022, random.randint(1, 12), random.randint(1, 28)),
                    'gpa': gpa,
                    'address': f"{i}00 Main Street",
                    'city': 'University City',
                    'state': 'State',
                    'country': 'Country',
                    'postal_code': '12345'
                }
            )
            if created:
                students_created += 1
                self.stdout.write(f"Created student: {student.full_name} ({student.roll_number})")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {students_created} students"))

        # Create Enrollments
        enrollments_created = 0
        students = Student.objects.all()
        for student in students[:10]:  # Enroll first 10 students
            num_courses = random.randint(3, 5)
            selected_courses = random.sample(courses, num_courses)

            for course in selected_courses:
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    semester='1st',
                    year=2024,
                    defaults={
                        'status': 'enrolled',
                        'attendance': random.randint(60, 100),
                        'midterm_score': round(random.uniform(50, 100), 2),
                        'final_score': round(random.uniform(50, 100), 2),
                        'assignment_score': round(random.uniform(50, 100), 2),
                    }
                )
                if created:
                    enrollments_created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully created {enrollments_created} enrollments"))

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
