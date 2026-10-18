from django import forms
from .models import Student, Course, Mark


class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = 'form-select' if isinstance(field.widget, forms.Select) else 'form-control'
            field.widget.attrs['class'] = css


class StudentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'admission_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class CourseForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class MarkForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model = Mark
        fields = '__all__'