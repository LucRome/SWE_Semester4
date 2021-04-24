from django import forms
from django.forms import ModelForm, Form, ChoiceField, IntegerField, CharField
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

class CourseStudentFilterForm(Form):
    matr_nr = IntegerField(label="Matrikel Nummer", required=False)
    username = CharField(max_length=50, label="Username", required=False)
    first_name = CharField(max_length=50, label="Vorname", required=False)
    last_name = CharField(max_length=50, label="Nachname", required=False)