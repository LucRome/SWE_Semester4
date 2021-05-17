from eCourse_backend.users.models import Lecturer
from django.test import TestCase
from django.contrib.auth.models import User
from http import HTTPStatus
from django.urls import reverse

from .views import *
from .models import *

from users.models import *
from users.forms import UserForm, StudentForm

from django.core.management import call_command


class FileExchangeTestCase(TestCase):
    def setUp(self):
        call_command('migrate')
        call_command('loadperms', 'groups.yml')
        self.my_admin = User.objects.create_superuser(
            'admin', 'admin@admin.com', 'admin123')

    @classmethod
    def setUpTestData(cls):
        lecturer_form = {
            'username': 'test_fe_lecturer',
            'first_name': 'Test_fe_lecturer',
            'last_name': 'Test_fe_lecturer',
            'email': 'test_fe_lecturer@test.com',
            'type': 2
        }
        Lecturer.objects.create(lecturer_form)


    def test_deny_anonymous_view_fileexchange(self):
        """
        Basically tests if the '@login_required' works/is set up everywhere
        """
        self.client.logout()

        response = self.client.get(reverse('overview'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(self.client.get(reverse('overview')),
            '/accounts/login/?next=/file_exchange/overview/')

        #response = self.client.get(reverse('create_exercise'), {}



    def test_filename_view(self):
        self.assertEqual(
            filename('upload/course_1/exercise_1/compilerbau_2019.pdf'),
            'compilerbau_2019.pdf')

        self.assertEqual(
            filename('upload/course_132113/exercise_1444444/_compilerbau_2019_harald.pdf'),
            '_compilerbau_2019_harald.pdf')
