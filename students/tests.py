from django.test import TestCase
from django.contrib.auth.models import User
from students.models import Student, Course, Program, Enrollment, Progress
from datetime import date


class StudentModelTest(TestCase):
    """Test cases for Student model"""
    
    def setUp(self):
        """Set up test data"""
        self.program = Program.objects.create(
            name='Computer Science',
            code='CS',
            duration_years=4
        )
        
        self.student = Student.objects.create(
            roll_number='CS0001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            program=self.program,
            admission_date=date.today()
        )
    
    def test_student_creation(self):
        """Test student creation"""
        self.assertEqual(self.student.full_name, 'John Doe')
        self.assertEqual(str(self.student), 'CS0001 - John Doe')
    
    def test_student_email_uniqueness(self):
        """Test email uniqueness constraint"""
        with self.assertRaises(Exception):
            Student.objects.create(
                roll_number='CS0002',
                first_name='Jane',
                last_name='Doe',
                email='john.doe@example.com',
                admission_date=date.today()
            )


class CourseModelTest(TestCase):
    """Test cases for Course model"""
    
    def setUp(self):
        """Set up test data"""
        self.course = Course.objects.create(
            name='Introduction to Python',
            code='CS101',
            credit_hours=3
        )
    
    def test_course_creation(self):
        """Test course creation"""
        self.assertEqual(str(self.course), 'CS101 - Introduction to Python')
        self.assertEqual(self.course.credit_hours, 3)


class EnrollmentModelTest(TestCase):
    """Test cases for Enrollment model"""
    
    def setUp(self):
        """Set up test data"""
        self.program = Program.objects.create(
            name='Computer Science',
            code='CS'
        )
        
        self.student = Student.objects.create(
            roll_number='CS0001',
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            program=self.program,
            admission_date=date.today()
        )
        
        self.course = Course.objects.create(
            name='Python Programming',
            code='CS101'
        )
        
        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course,
            semester='1st',
            year=2024,
            midterm_score=85,
            final_score=90,
            assignment_score=88,
            attendance=95
        )
    
    def test_enrollment_grade_calculation(self):
        """Test grade calculation"""
        # (85*0.30) + (90*0.50) + (88*0.15) + (95*0.05) = 88.65
        expected_score = (85*0.30) + (90*0.50) + (88*0.15) + (95*0.05)
        self.assertAlmostEqual(self.enrollment.total_score, expected_score, places=2)
    
    def test_enrollment_letter_grade(self):
        """Test letter grade assignment"""
        self.assertEqual(self.enrollment.grade, 'A')
