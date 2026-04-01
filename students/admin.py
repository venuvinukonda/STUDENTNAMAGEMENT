from django.contrib import admin
from .models import Student, Course, Enrollment, Program, Progress


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'duration_years', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['duration_years', 'created_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'credit_hours', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['credit_hours', 'created_at']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_number', 'first_name', 'last_name', 'email', 'program', 'semester', 'status', 'gpa']
    search_fields = ['roll_number', 'first_name', 'last_name', 'email']
    list_filter = ['status', 'semester', 'program', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('roll_number', 'first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'gender')
        }),
        ('Academic Information', {
            'fields': ('program', 'semester', 'status', 'admission_date', 'gpa')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code'),
            'classes': ('collapse',)
        }),
        ('Emergency Contact', {
            'fields': ('guardian_name', 'guardian_phone'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'semester', 'year', 'status', 'grade', 'total_score']
    search_fields = ['student__roll_number', 'course__code']
    list_filter = ['status', 'semester', 'year', 'course']
    readonly_fields = ['enrolled_date', 'updated_at']


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'semester', 'year', 'semester_gpa', 'cumulative_gpa', 'courses_passed', 'courses_failed']
    search_fields = ['student__roll_number']
    list_filter = ['year', 'semester', 'academic_warning', 'probation_status']
    readonly_fields = ['created_at', 'updated_at']
