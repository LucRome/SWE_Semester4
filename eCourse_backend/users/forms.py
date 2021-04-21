from django.forms import ModelForm, Form, ChoiceField, CharField
from users.models import User, Student, Lecturer, Office


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'matr_nr']


# useradministration: filter forms

class LecturerFilterForm(Form):
    first_name = CharField(max_length=50, label="Vorname", required=False)
    last_name = CharField(max_length=50, label="Nachname", required=False)
