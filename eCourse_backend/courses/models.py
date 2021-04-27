from django.db import models
from users.models import Lecturer, Student

# Create your models here.


class Course(models.Model):
    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.CASCADE,
        related_name='courses')
    student = models.ManyToManyField(Student)
    name = models.CharField(max_length=32)
    start_date = models.DateField()
    end_date = models.DateField()


class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    description = models.TextField()
    start_time = models.DateTimeField()
    work_time_duration = models.DurationField()
    submission_deadline = models.DateTimeField()
    is_visible = models.BooleanField(default=False)
    is_evaluated = models.BooleanField(default=False)
    description = models.TextField(default=None)
