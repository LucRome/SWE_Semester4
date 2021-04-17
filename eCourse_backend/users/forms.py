from django.forms import ModelForm, Form, ChoiceField, CharField, IntegerField
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


# useradministration: filter forms

class LecturerFilterForm(Form):
    username = CharField(max_length=50, label="Username", required=False)
    first_name = CharField(max_length=50, label="Vorname", required=False)
    last_name = CharField(max_length=50, label="Nachname", required=False)


class StudentFilterForm(Form):
    matr_nr = IntegerField(label="Matrikel Nummer", required=False)
    username = CharField(max_length=50, label="Username", required=False)
    first_name = CharField(max_length=50, label="Vorname", required=False)
    last_name = CharField(max_length=50, label="Nachname", required=False)


class AdminStaffFilterForm(Form):
    username = CharField(max_length=50, label="Username", required=False)
    first_name = CharField(max_length=50, label="Vorname", required=False)
    last_name = CharField(max_length=50, label="Nachname", required=False)
