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
        call_command('migrate')
        call_command('loadperms', 'groups.yml')
        self.my_admin = User.objects.create_superuser(
            'admin', 'admin@admin.com', 'admin123')

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
            'username': 'testerino',
            'first_name': 'Testvorname',
            'last_name': 'Testnachname',
            'email': 'test@test.com',
            'matr_nr': '69420'
        }
        user = StudentForm(student_form)
        # There is no way (yet) the creation could fail right?
        self.assertTrue(user.is_valid())
        user.save()

        self.assertTrue(Student.objects.filter(username='testerino').exists())

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

        self.assertTrue(Lecturer.objects.filter(
            username='testerino3').exists())
        self.assertTrue(Lecturer.objects.get(username='testerino3').type == 2)

    def test_create_officeuser_view(self):
        self.client.force_login(self.my_admin)

        user_form = {
            'username': 'testerino4',
            'first_name': 'Testvorname4',
            'last_name': 'Testnachname4',
            'email': 'test4@test.com'
        }

        response = self.client.post(
            reverse('createofficeuser_admin_iframe'), user_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTrue(Office.objects.filter(
            username='testerino4').exists())
        self.assertTrue(Office.objects.get(username='testerino4').type == 1)

    def test_create_student_view(self):
        self.client.force_login(self.my_admin)

        user_form = {
            'username': 'testerino5',
            'first_name': 'Testvorname5',
            'last_name': 'Testnachname5',
            'email': 'test5@test.com',
            'matr_nr': '69420',
        }

        response = self.client.post(
            reverse('createstudent_admin_iframe'), user_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTrue(Student.objects.filter(
            username='testerino5').exists())
        self.assertTrue(Student.objects.get(username='testerino5').type == 3)

    def test_list_student_view(self):
        self.client.force_login(self.my_admin)

        response = self.client.post(
            reverse('studentlist_admin_iframe', kwargs={'page': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_lecturer_view(self):
        self.client.force_login(self.my_admin)

        response = self.client.post(
            reverse('lecturerlist_admin_iframe', kwargs={'page': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_list_admin_view(self):
        self.client.force_login(self.my_admin)

        response = self.client.post(
            reverse('adminlist_admin_iframe', kwargs={'page': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_user_view(self):
        self.client.force_login(self.my_admin)

        user_form = {
            'username': 'testerino1',
            'first_name': 'Testvorname1',
            'last_name': 'Testnachname1',
            'email': 'test1@test.com',
            'matr_nr': '69421000',
        }

        response = self.client.post(
            reverse('createstudent_admin_iframe'), user_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTrue(Student.objects.filter(
            username='testerino1').exists())
        self.assertTrue(Student.objects.get(username='testerino1').type == 3)

        my_id = Student.objects.get(username='testerino1').id
        response = self.client.post(
            reverse('edituser_admin_modalcontent_iframe', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_delete_user_view(self):
        self.client.force_login(self.my_admin)

        user_form = {
            'username': 'testerino0',
            'first_name': 'Testvorname0',
            'last_name': 'Testnachname0',
            'email': 'test0@test.com',
            'matr_nr': '69420000',
        }

        response = self.client.post(
            reverse('createstudent_admin_iframe'), user_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTrue(Student.objects.filter(
            username='testerino0').exists())
        self.assertTrue(Student.objects.get(username='testerino0').type == 3)

        my_id = Student.objects.get(username='testerino0').id
        response = self.client.post(
            reverse('deleteuser_admin_iframe', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Student.objects.filter(
            username='testerino0').exists())
