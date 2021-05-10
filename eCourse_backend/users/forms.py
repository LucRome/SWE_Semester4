from django.forms import ModelForm, Form, ChoiceField, CharField, IntegerField, PasswordInput, HiddenInput
import string, random
from users.models import User, Student, Lecturer, Office

def get_random_pw():
    return ''.join(random.SystemRandom().choices(string.ascii_uppercase + string.digits, k=15))

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': HiddenInput(attrs={'id': 'defaultPWField', 'value': get_random_pw()})
        }

class StudentForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'matr_nr', 'password']
        widgets = {
            'password': HiddenInput(attrs={'id': 'defaultPWField', 'value': get_random_pw()})
        }
        
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
