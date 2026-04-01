from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Students
    path('students/', views.StudentListView.as_view(), name='student-list'),
    path('students/create/', views.StudentCreateView.as_view(), name='student-create'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student-edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
    
    # Courses
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course-edit'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    
    # Programs
    path('programs/', views.ProgramListView.as_view(), name='program-list'),
    path('programs/create/', views.ProgramCreateView.as_view(), name='program-create'),
    path('programs/<int:pk>/edit/', views.ProgramUpdateView.as_view(), name='program-edit'),
    path('programs/<int:pk>/delete/', views.ProgramDeleteView.as_view(), name='program-delete'),
    
    # Enrollments
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment-list'),
    path('enrollments/create/', views.EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollments/<int:pk>/edit/', views.EnrollmentUpdateView.as_view(), name='enrollment-edit'),
    path('enrollments/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment-delete'),
    
    # Grades
    path('grades/', views.grade_list, name='grade-list'),
    path('grades/<int:enrollment_id>/update/', views.update_grades, name='update-grades'),
    
    # Reports
    path('reports/', views.reports, name='reports'),
    
    # API
    path('api/student/<int:student_id>/progress/', views.get_student_progress, name='api-student-progress'),
    path('api/student/<int:student_id>/enrollments/', views.get_student_enrollments, name='api-student-enrollments'),
]
