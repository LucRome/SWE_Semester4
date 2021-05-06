from django.forms import ModelForm, Form, ChoiceField
from users.models import User, Student, Lecturer, Office


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'matr_nr']


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'matr_nr']


class LecturerForm(ModelForm):
    class Meta:
        model = Lecturer
        fields = ['username', 'first_name', 'last_name', 'email', 'matr_nr']


class OfficeUserForm(ModelForm):
    class Meta:
        model = Office
        fields = ['username', 'first_name', 'last_name', 'email', 'matr_nr']


class UsertypeChooseForm(Form):
    CHOICES = [
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('office', 'Office User'),
    ]

    user_type = ChoiceField(choices=CHOICES)
