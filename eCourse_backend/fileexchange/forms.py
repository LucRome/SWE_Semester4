from django import forms
from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration
from users.models import Lecturer
from .models import Submission
from courses.models import Exercise

# DatetTime input fields
# showing little calendar to choose date and time


class SD_DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


# duration field
# converting user input to valid duration
class DurationInput(TextInput):

    def _format_value(self, value):
        duration = parse_duration(value)
        seconds = duration.seconds
        minutes = seconds // 60
        seconds = seconds % 60
        minutes = minutes % 60

        return '{:02d}:{:02d}'.format(minutes, seconds)


class FileForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['exercise', 'name', 'file']


class ExersiceForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'
        widgets = {
            'start_time': SD_DateTimeInput(format=['%Y-%m-%d']),
            'submission_deadline': SD_DateTimeInput(format=['%Y-%m-%d']),
            'work_time_duration': DurationInput()
        }
