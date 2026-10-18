from django.contrib import admin
from .models import Department, Course, Student, Attendance, Mark


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'credits')
    list_filter = ('department',)
    search_fields = ('code', 'name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'first_name', 'last_name', 'department', 'year')
    list_filter = ('department', 'year')
    search_fields = ('roll_no', 'first_name', 'last_name', 'email')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')
    list_filter = ('course', 'date', 'status')


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'exam_type', 'marks_obtained', 'max_marks')
    list_filter = ('course', 'exam_type')