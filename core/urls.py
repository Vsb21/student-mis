from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/add/', views.StudentCreateView.as_view(), name='student_add'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', views.StudentUpdateView.as_view(), name='student_edit'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),

    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/add/', views.CourseCreateView.as_view(), name='course_add'),
    path('courses/<int:pk>/edit/', views.CourseUpdateView.as_view(), name='course_edit'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    path('attendance/', views.mark_attendance, name='mark_attendance'),

    path('marks/', views.MarkListView.as_view(), name='mark_list'),
    path('marks/add/', views.MarkCreateView.as_view(), name='mark_add'),
    path('marks/<int:pk>/edit/', views.MarkUpdateView.as_view(), name='mark_edit'),
    path('marks/<int:pk>/delete/', views.MarkDeleteView.as_view(), name='mark_delete'),
]