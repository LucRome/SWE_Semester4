from django.db import models
from django.contrib.auth.models import AbstractUser

def exercise_directory_path(instance, filename):
        return '/upload/course_{0}/exercise_{1}/{2}'.format(instance.exercise.course.id, instance.exercise.id, filename)

class User(AbstractUser):
    """
    This class represents the different types of users.
    The three different groups of users are:

    - student
    - lecturer
    - administrator/superuser
    - staff

    The class is derived from django's AbstracUser. Hence it only additionally needs the matr_nr field.
    """
    matr_nr =  models.IntegerField(default=0)

class Course(models.Model):
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ManyToManyField(User)
    name = models.CharField(max_length=32)
    start_date = models.DateField()
    end_date = models.DateField()

class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    work_time_duration = models.DurationField()
    submission_deadline = models.DateTimeField()
    is_visible = models.BooleanField(default=False)
    is_evaluated = models.BooleanField(default=False)
    
class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField()
    upload_time = models.DateTimeField()
    file = models.FileField(upload_to=exercise_directory_path)