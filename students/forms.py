from django import forms
from .models import Student, Course, Enrollment, Program, Progress


class StudentForm(forms.ModelForm):
    """Form for creating and updating students"""
    class Meta:
        model = Student
        fields = [
            'roll_number', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'program', 'semester', 'status',
            'admission_date', 'address', 'city', 'state', 'country',
            'postal_code', 'guardian_name', 'guardian_phone'
        ]
        widgets = {
            'roll_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter roll number'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'program': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admission_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': 'Enter address'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'State/Province'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Postal code'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Guardian name'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Guardian phone'}),
        }


class EnrollmentForm(forms.ModelForm):
    """Form for creating and updating enrollments"""
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'semester', 'year', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class GradeForm(forms.ModelForm):
    """Form for updating grades and attendance"""
    class Meta:
        model = Enrollment
        fields = ['attendance', 'midterm_score', 'final_score', 'assignment_score', 'status']
        widgets = {
            'attendance': forms.NumberInput(attrs={'class': 'form-input', 'min': '0', 'max': '100'}),
            'midterm_score': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'max': '100'}),
            'final_score': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'max': '100'}),
            'assignment_score': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0', 'max': '100'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class ProgramForm(forms.ModelForm):
    """Form for creating and updating programs"""
    class Meta:
        model = Program
        fields = ['name', 'code', 'duration_years']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Program code'}),
            'duration_years': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
        }


class CourseForm(forms.ModelForm):
    """Form for creating and updating courses"""
    class Meta:
        model = Course
        fields = ['name', 'code', 'credit_hours', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Course name'}),
            'code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Course code'}),
            'credit_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': '1'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': 'Course description'}),
        }
