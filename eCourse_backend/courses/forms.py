from django import forms
from users.models import Student
from .models import Course


class CourseForm(forms.ModelForm):
    student = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Course
        fields = '__all__'
    # TODO: Add students in extra window or in js? Filter functions etc
