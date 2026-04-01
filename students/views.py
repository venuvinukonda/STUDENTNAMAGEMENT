from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from django.http import JsonResponse
from datetime import datetime

from .models import Student, Course, Enrollment, Program, Progress
from .forms import StudentForm, EnrollmentForm, GradeForm, ProgramForm, CourseForm


# Dashboard Views
def dashboard(request):
    """Main dashboard view"""
    context = {
        'total_students': Student.objects.count(),
        'active_students': Student.objects.filter(status='active').count(),
        'total_courses': Course.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
    }
    return render(request, 'students/dashboard.html', context)


# Student Views
class StudentListView(ListView):
    """List all students"""
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20

    def get_queryset(self):
        queryset = Student.objects.all()
        search = self.request.GET.get('search')
        status = self.request.GET.get('status')
        semester = self.request.GET.get('semester')
        
        if search:
            queryset = queryset.filter(
                Q(roll_number__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if status:
            queryset = queryset.filter(status=status)
        
        if semester:
            queryset = queryset.filter(semester=semester)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Student.STATUS_CHOICES
        context['semester_choices'] = Student.SEMESTER_CHOICES
        return context


class StudentDetailView(DetailView):
    """View student details"""
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        context['enrollments'] = Enrollment.objects.filter(student=student)
        context['progress_records'] = Progress.objects.filter(student=student)
        return context


class StudentCreateView(CreateView):
    """Create a new student"""
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')


class StudentUpdateView(UpdateView):
    """Update student information"""
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('student-list')


class StudentDeleteView(DeleteView):
    """Delete a student"""
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('student-list')


# Course Views
class CourseListView(ListView):
    """List all courses"""
    model = Course
    template_name = 'students/course_list.html'
    context_object_name = 'courses'
    paginate_by = 20


class CourseCreateView(CreateView):
    """Create a new course"""
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('course-list')


class CourseUpdateView(UpdateView):
    """Update course information"""
    model = Course
    form_class = CourseForm
    template_name = 'students/course_form.html'
    success_url = reverse_lazy('course-list')


class CourseDeleteView(DeleteView):
    """Delete a course"""
    model = Course
    template_name = 'students/course_confirm_delete.html'
    success_url = reverse_lazy('course-list')


# Enrollment Views
class EnrollmentListView(ListView):
    """List all enrollments"""
    model = Enrollment
    template_name = 'students/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 20

    def get_queryset(self):
        queryset = Enrollment.objects.select_related('student', 'course')
        status = self.request.GET.get('status')
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset


class EnrollmentCreateView(CreateView):
    """Create a new enrollment"""
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'students/enrollment_form.html'
    success_url = reverse_lazy('enrollment-list')


class EnrollmentUpdateView(UpdateView):
    """Update enrollment information"""
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'students/enrollment_form.html'
    success_url = reverse_lazy('enrollment-list')


class EnrollmentDeleteView(DeleteView):
    """Delete an enrollment"""
    model = Enrollment
    template_name = 'students/enrollment_confirm_delete.html'
    success_url = reverse_lazy('enrollment-list')


# Grade Views
def grade_list(request):
    """List enrollments for grade management"""
    enrollments = Enrollment.objects.select_related('student', 'course')
    
    student_id = request.GET.get('student')
    course_id = request.GET.get('course')
    
    if student_id:
        enrollments = enrollments.filter(student_id=student_id)
    
    if course_id:
        enrollments = enrollments.filter(course_id=course_id)
    
    context = {
        'enrollments': enrollments,
        'students': Student.objects.all(),
        'courses': Course.objects.all(),
    }
    return render(request, 'students/grade_list.html', context)


def update_grades(request, enrollment_id):
    """Update grades for an enrollment"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('enrollment-list')
    else:
        form = GradeForm(instance=enrollment)
    
    context = {
        'form': form,
        'enrollment': enrollment,
    }
    return render(request, 'students/update_grades.html', context)


# Program Views
class ProgramListView(ListView):
    """List all programs"""
    model = Program
    template_name = 'students/program_list.html'
    context_object_name = 'programs'


class ProgramCreateView(CreateView):
    """Create a new program"""
    model = Program
    form_class = ProgramForm
    template_name = 'students/program_form.html'
    success_url = reverse_lazy('program-list')


class ProgramUpdateView(UpdateView):
    """Update program information"""
    model = Program
    form_class = ProgramForm
    template_name = 'students/program_form.html'
    success_url = reverse_lazy('program-list')


class ProgramDeleteView(DeleteView):
    """Delete a program"""
    model = Program
    template_name = 'students/program_confirm_delete.html'
    success_url = reverse_lazy('program-list')


# API Views for AJAX
def get_student_progress(request, student_id):
    """API endpoint to get student progress"""
    student = get_object_or_404(Student, id=student_id)
    progress_records = Progress.objects.filter(student=student).order_by('-year', 'semester').values(
        'id', 'semester', 'year', 'semester_gpa', 'cumulative_gpa', 'courses_passed', 'courses_failed'
    )
    
    return JsonResponse({
        'success': True,
        'student': student.full_name,
        'progress_records': list(progress_records)
    })


def get_student_enrollments(request, student_id):
    """API endpoint to get student enrollments"""
    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student).select_related('course').values(
        'id', 'course__code', 'course__name', 'status', 'semester', 'year', 'attendance', 'midterm_score', 'final_score'
    )
    
    return JsonResponse({
        'success': True,
        'enrollments': list(enrollments)
    })


def reports(request):
    """Generate reports"""
    # Top performing students
    top_students = Student.objects.order_by('-gpa')[:10]
    
    # Students on academic warning
    warning_students = Student.objects.filter(gpa__lt=2.0)
    
    # Enrollment statistics
    total_enrollments = Enrollment.objects.count()
    completed_enrollments = Enrollment.objects.filter(status='completed').count()
    
    # Calculate completion rate
    completion_rate = (completed_enrollments / total_enrollments * 100) if total_enrollments > 0 else 0
    
    context = {
        'top_students': top_students,
        'warning_students': warning_students,
        'total_enrollments': total_enrollments,
        'completed_enrollments': completed_enrollments,
        'completion_rate': round(completion_rate, 1),
    }
    
    return render(request, 'students/reports.html', context)
