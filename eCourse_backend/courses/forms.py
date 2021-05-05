from django import forms
from users.models import Lecturer
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
    # TODO: Add students in extra window or in js? Filter functions etc
