from django.utils import timezone
from django.db import models
from users.models import User
from courses.models import Exercise, Course


def exercise_directory_path(instance, filename):
    return './upload/course_{0}/exercise_{1}/{2}'.format(
        instance.exercise.course.id, instance.exercise.id, filename)


class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    #description = models.TextField()
    upload_time = models.DateTimeField()
    file = models.FileField(upload_to=exercise_directory_path)

    def save(self):
        self.upload_time = timezone.now()
        super(Submission, self).save()
