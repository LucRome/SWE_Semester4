from datetime import datetime
from django import forms
from django.forms import TextInput, MultiWidget, DateTimeField
from django.contrib.admin import widgets
from django.utils.dateparse import parse_duration
from django.utils.timezone import make_aware
from users.models import Lecturer
from .models import Submission
from courses.models import Exercise


# source:
# https://gist.github.com/andytwoods/76f18f5ddeba9192d51dccc922086e43?fbclid=IwAR1x4GbeHLMQypWKaYPGn55r92-uCmJZqLUf4kEAGeX4DTgalt2GQUNY7oQ
class DateTimeMultiWidget(MultiWidget):

    def __init__(self, widgets=None, attrs=None):
        if widgets is None:
            if attrs is None:
                attrs = {}
            date_attrs = attrs.copy()
            time_attrs = attrs.copy()

            date_attrs['type'] = 'date'
            time_attrs['type'] = 'time'

            widgets = [
                TextInput(attrs=date_attrs),
                TextInput(attrs=time_attrs),
            ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.strftime('%H:%M')]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        date_str, time_str = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.

        if date_str == time_str == '':
            return None

        if time_str == '':
            time_str = '00:00'

        my_datetime = datetime.strptime(
            date_str + ' ' + time_str, "%Y-%m-%d %H:%M")
        # making timezone aware
        return make_aware(my_datetime)


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
        fields = ['name', 'file']
        labels = {
            'name': 'Name',
            'file': 'Datei'
        }


class ExersiceForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = '__all__'
        widgets = {
            'start_time': DateTimeMultiWidget(),
            'submission_deadline': DateTimeMultiWidget(),
            'work_time_duration': DurationInput()
        }
        labels = {
            'course': 'Kurs',
            'description': 'Beschreibung',
            'start_time': 'Startzeit',
            'work_time_duration': 'Bearbeitungszeit',
            'submission_deadline': 'Deadline',
            'is_visible': 'sichtbar',
            'is_evaluated': 'benotet',
            'description': 'Beschreibung'
        }
