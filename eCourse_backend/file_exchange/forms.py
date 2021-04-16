from django import forms
from users.models import Lecturer
from .models import Submission


class FileForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'
