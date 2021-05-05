from django.forms import ModelForm, Form, ChoiceField, CharField, IntegerField
from users.models import User, Student, Lecturer, Office


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class StudentForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'matr_nr']

# useradministration: filter forms


class LecturerAndOfficeFilterForm(Form):
    username = CharField(max_length=50, label='Username',
                         initial='', required=False)
    first_name = CharField(max_length=50, label='Vorname',
                           initial='', required=False)
    last_name = CharField(max_length=50, label='Nachname',
                          initial='', required=False)


class StudentFilterForm(LecturerAndOfficeFilterForm):
    matr_nr = IntegerField(label='Matrikel Nummer', initial='', required=False)
