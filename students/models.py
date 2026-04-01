from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Program(models.Model):
    """Model for degree programs"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    duration_years = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Course(models.Model):
    """Model for courses"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    credit_hours = models.IntegerField(default=3)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ['code']


class Student(models.Model):
    """Model for students"""
    SEMESTER_CHOICES = [
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('3rd', '3rd Semester'),
        ('4th', '4th Semester'),
        ('5th', '5th Semester'),
        ('6th', '6th Semester'),
        ('7th', '7th Semester'),
        ('8th', '8th Semester'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
    ]

    # Basic Information
    roll_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)

    # Academic Information
    program = models.ForeignKey(Program, on_delete=models.PROTECT, null=True, blank=True)
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='1st')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    admission_date = models.DateField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00,
                              validators=[MinValueValidator(0.0), MaxValueValidator(4.0)])

    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    # Emergency Contact
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_phone = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.roll_number} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['roll_number']
        indexes = [
            models.Index(fields=['roll_number']),
            models.Index(fields=['email']),
        ]


class Enrollment(models.Model):
    """Model for student course enrollments"""
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='enrollments')
    semester = models.CharField(max_length=10)
    year = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrolled')
    
    # Grades
    attendance = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    midterm_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, 
                                        validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_score = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                     validators=[MinValueValidator(0), MaxValueValidator(100)])
    assignment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                          validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    enrolled_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'course', 'semester', 'year']
        ordering = ['-year', 'semester', 'course']

    def __str__(self):
        return f"{self.student.roll_number} - {self.course.code}"

    @property
    def total_score(self):
        """Calculate weighted total score"""
        return (
            (self.midterm_score * Decimal('0.30')) +
            (self.final_score * Decimal('0.50')) +
            (self.assignment_score * Decimal('0.15')) +
            (self.attendance * Decimal('0.05'))
        )

    @property
    def grade(self):
        """Calculate letter grade based on total score"""
        score = self.total_score
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


class Progress(models.Model):
    """Model for tracking student progress"""
    PERIOD_CHOICES = [
        ('semester', 'Semester'),
        ('year', 'Year'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress_records')
    semester = models.CharField(max_length=10)
    year = models.IntegerField()
    period_type = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='semester')
    
    # Academic Performance
    total_credits_completed = models.IntegerField(default=0)
    courses_passed = models.IntegerField(default=0)
    courses_failed = models.IntegerField(default=0)
    semester_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    cumulative_gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    
    # Attendance
    total_classes = models.IntegerField(default=0)
    classes_attended = models.IntegerField(default=0)
    
    # Warnings
    academic_warning = models.BooleanField(default=False)
    probation_status = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'semester', 'year']
        ordering = ['-year', 'semester']

    def __str__(self):
        return f"{self.student.roll_number} - {self.semester} {self.year}"

    @property
    def attendance_percentage(self):
        if self.total_classes == 0:
            return 0
        return (self.classes_attended / self.total_classes) * 100
