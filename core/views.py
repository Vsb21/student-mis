from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CourseForm, MarkForm, StudentForm
from .models import Attendance, Course, Department, Mark, Student


@login_required
def dashboard(request):
    context = {
        'student_count': Student.objects.count(),
        'course_count': Course.objects.count(),
        'department_count': Department.objects.count(),
        'recent_students': Student.objects.order_by('-id')[:5],
    }
    return render(request, 'core/dashboard.html', context)


# ---------- Students ----------
class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'core/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        qs = Student.objects.select_related('department')
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(
                Q(roll_no__icontains=q) | Q(first_name__icontains=q)
                | Q(last_name__icontains=q) | Q(email__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        return ctx


class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'core/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = self.object
        total = student.attendance.count()
        present = student.attendance.filter(status='P').count()
        ctx['marks'] = student.marks.select_related('course')
        ctx['attendance_total'] = total
        ctx['attendance_present'] = present
        ctx['attendance_percent'] = round(present / total * 100, 1) if total else 0
        return ctx


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('student_list')
    extra_context = {'title': 'Add Student'}

    def form_valid(self, form):
        messages.success(self.request, 'Student added.')
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('student_list')
    extra_context = {'title': 'Edit Student'}

    def form_valid(self, form):
        messages.success(self.request, 'Student updated.')
        return super().form_valid(form)


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Student deleted.')
        return super().form_valid(form)


# ---------- Courses ----------
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'core/course_list.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.select_related('department')


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('course_list')
    extra_context = {'title': 'Add Course'}


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('course_list')
    extra_context = {'title': 'Edit Course'}


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('course_list')


# ---------- Attendance ----------
@login_required
def mark_attendance(request):
    courses = Course.objects.select_related('department')
    course_id = request.GET.get('course') or request.POST.get('course')
    date_str = request.GET.get('date') or request.POST.get('date') or str(date.today())
    course = None
    students = []

    if course_id:
        course = get_object_or_404(Course, pk=course_id)
        students = list(Student.objects.filter(department=course.department))
        existing = {
            a.student_id: a.status
            for a in Attendance.objects.filter(course=course, date=date_str)
        }
        for s in students:
            s.current_status = existing.get(s.id, 'P')

    if request.method == 'POST' and course:
        for s in students:
            status = request.POST.get(f'status_{s.id}', 'A')
            Attendance.objects.update_or_create(
                student=s, course=course, date=date_str, defaults={'status': status}
            )
        messages.success(request, 'Attendance saved.')
        return redirect(f"{reverse('mark_attendance')}?course={course.id}&date={date_str}")

    return render(request, 'core/attendance.html', {
        'courses': courses, 'course': course, 'students': students, 'date': date_str,
    })


# ---------- Marks ----------
class MarkListView(LoginRequiredMixin, ListView):
    model = Mark
    template_name = 'core/mark_list.html'
    context_object_name = 'marks'
    paginate_by = 15

    def get_queryset(self):
        return Mark.objects.select_related('student', 'course')


class MarkCreateView(LoginRequiredMixin, CreateView):
    model = Mark
    form_class = MarkForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('mark_list')
    extra_context = {'title': 'Add Marks'}


class MarkUpdateView(LoginRequiredMixin, UpdateView):
    model = Mark
    form_class = MarkForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('mark_list')
    extra_context = {'title': 'Edit Marks'}


class MarkDeleteView(LoginRequiredMixin, DeleteView):
    model = Mark
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('mark_list')