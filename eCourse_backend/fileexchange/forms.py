from django import forms
from django.forms.widgets import TextInput
from django.forms import MultiWidget
from django.contrib.admin import widgets
from django.utils.dateparse import parse_duration
from users.models import Lecturer
from .models import Submission
from courses.models import Exercise

# DatetTime input fields
# showing little calendar to choose date and time


# class DateTimeInput(forms.MultiWidget()):
#     # input_type = 'datetime-local'

#     # def __init__(self, **kwargs):
#     #     kwargs["format"] = "%Y-%m-%dT%H:%M"
#     #     super().__init__(**kwargs)

#     # def decompress(self, value):
#     #     if value:
#     #         return [value.date(), value.time().replace(microsecond=0)]
#     #     return [None, None]
#     def __init__(self, attr = None):
#         widgets = [forms.DateField, forms.TimeField]

class _Date(forms.DateInput):
    input_type = 'date'

    def __init__(self, **kwargs):
        kwargs['format'] = '%Y-%m-%d'
        super().__init__(**kwargs)

class _Time(forms.DateInput):
    input_type = 'time'

    def __init__(self, **kwargs):
        kwargs['format'] = '%H:%M'
        super().__init__(**kwargs)

class DateTime(forms.MultiWidget):
    def __init__(self, attrs = None):
        widgets = [
            _Date(format = ['%Y-%m-%d']),
            _Time(format = ['%H:%M'])
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond = 0).replace(milisecond = 0).replace(second = 0)]
        return [None, None]

    


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
            'start_time': DateTime(),
            'submission_deadline': DateTime(),
            'work_time_duration': DurationInput()
        }
