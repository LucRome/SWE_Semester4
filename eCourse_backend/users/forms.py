from django.forms import ModelForm
from users.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'matr_nr']
    # TODO: Add users to courses
