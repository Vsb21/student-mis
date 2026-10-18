from django.db import models


class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Course(models.Model):
    code = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    credits = models.PositiveSmallIntegerField(default=3)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Student(models.Model):
    YEAR_CHOICES = [(1, 'First Year'), (2, 'Second Year'), (3, 'Third Year'), (4, 'Fourth Year')]

    roll_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    dob = models.DateField(verbose_name='Date of birth')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='students')
    year = models.PositiveSmallIntegerField(choices=YEAR_CHOICES, default=1)
    address = models.TextField(blank=True)
    admission_date = models.DateField()

    class Meta:
        ordering = ['roll_no']

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.roll_no} - {self.full_name}"


class Attendance(models.Model):
    STATUS_CHOICES = [('P', 'Present'), ('A', 'Absent')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    class Meta:
        unique_together = ('student', 'course', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.roll_no} {self.course.code} {self.date} {self.status}"


class Mark(models.Model):
    EXAM_CHOICES = [('MID', 'Mid Term'), ('END', 'End Term'), ('INT', 'Internal'), ('LAB', 'Lab')]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='marks')
    exam_type = models.CharField(max_length=3, choices=EXAM_CHOICES)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100)

    class Meta:
        unique_together = ('student', 'course', 'exam_type')
        ordering = ['student__roll_no', 'course__code']

    @property
    def percentage(self):
        if self.max_marks:
            return round(self.marks_obtained / self.max_marks * 100, 1)
        return 0

    def __str__(self):
        return f"{self.student.roll_no} {self.course.code} {self.exam_type}"