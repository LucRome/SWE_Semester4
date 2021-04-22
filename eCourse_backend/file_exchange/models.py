import os
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from users.models import User
from courses.models import Exercise, Course

# upload dir
def exercise_directory_path(instance, filename):
    return 'upload/course_{0}/exercise_{1}/{2}'.format(
        instance.exercise.course.id, instance.exercise.id, filename)


# validate file type
def validate_file_type(file):
    extension = os.path.splitext(file.name)[1]
    valid_extensions = ['.pdf']
    if extension not in valid_extensions:
        raise ValidationError(u'File not supportet')


class Submission(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    upload_time = models.DateTimeField()
    file = models.FileField(
        upload_to=exercise_directory_path,
        validators=[validate_file_type])

    def save(self):
        self.upload_time = timezone.now()
        super(Submission, self).save()
