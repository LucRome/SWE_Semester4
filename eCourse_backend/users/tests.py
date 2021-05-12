from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError

from .models import *
from .views import *

from django.core.management import call_command


# Create your tests here.
# TESTS MUST ALWAYS START WITH "test"!

class UserTestCase(TestCase):
    def setUp(self):
        call_command('loadperms', 'groups.yml')
        self.my_admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')  


    def test_deny_anonymous_view_user(self):
        """
        Basically tests if the '@login_required' works/is set up everywhere
        """
        self.client.logout()

        # check the URLs that need no parameters
        response = self.client.get(reverse('user_administration'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        
        response = self.client.get(reverse('createlecturer_admin_iframe'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 404

        """
        # check the URLs that need an object/ID
        response = self.client.get(reverse('deleteuser_admin_iframe'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 404

        response = self.client.get(reverse('edituser_admin_modalcontent_iframe'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 404
        """

    def test_create_student_form(self):
        student_form = {
            'username' : 'testerino',
            'first_name' : 'Testvorname',
            'last_name' : 'Testnachname',
            'email' : 'test@test.com',
            'matr_nr' : '69420'
        }
        user = StudentForm(student_form)
        # There is no way (yet) the creation could fail right?
        self.assertTrue(user.is_valid())
        user.save()

        self.assertTrue(Student.objects.filter(username='testerino').exists())

    """
    def test_create_user_view_url_check_db(self):
        my_admin = User.objects.create_superuser(
            'admin', 'admin@admin.com', 'admin123')
        # my_admin.set_password('admin123')
        my_admin.save()

        self.assertTrue(my_admin.is_superuser)
        self.assertFalse(my_admin.is_authenticated)
        self.client.force_login(my_admin)
        self.assertTrue(my_admin.is_authenticated)

        user_form = {
            'username' : 'testerino2',
            'first_name' : 'Testvorname2',
            'last_name' : 'Testnachname2',
            'email' : 'test2@test.com',
            'matr_nr' : '42069'
        }
        response = self.client.post('/users/create', user_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # query_set = User.objects.filter(username='testerino2')
        query_set = User.objects.all()
        print(query_set)
        self.assertIn('testerino2', query_set)
    """

    def test_create_lecturer_view(self):
        self.client.force_login(self.my_admin)

        user_form = {
            'username': 'testerino3',
            'first_name': 'Testvorname3',
            'last_name': 'Testnachname3',
            'email': 'test3@test.com'
        }

        response = self.client.post(
            reverse('createlecturer_admin_iframe'), user_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        query_set = Lecturer.objects.all()
        self.assertTrue(Lecturer.objects.filter(username='testerino3').exists())
