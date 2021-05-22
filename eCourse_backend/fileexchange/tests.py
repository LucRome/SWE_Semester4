from django.test import TestCase, RequestFactory
from unittest import mock
from django.contrib.auth.models import User
from http import HTTPStatus
from django.urls import reverse
from django.utils.dateparse import parse_duration, parse_datetime

from .views import *
from .models import *
from users.models import *
from users.views import *

#from users.models import *
#from users.forms import UserForm, StudentForm

from .forms import FileForm, ExersiceForm
from courses.models import Exercise, Course

from django.core.management import call_command


class FileExchangeTestCase(TestCase):
    def setUp(self):
        call_command('migrate')
        call_command('loadperms', 'groups.yml')
        self.my_admin = User.objects.create_superuser(
            'admin', 'admin@admin.com', 'admin123')

        self.client.force_login(self.my_admin)

        # create users to do stuff with in the tests
        lecturer_form = {
            'username': 'test_fe_lecturer',
            'first_name': 'Test_fe_lecturer',
            'last_name': 'Test_fe_lecturer',
            'email': 'test_fe_lecturer@test.com',
            'password': '12345',
        }
        response = self.client.post(
            reverse('createlecturer_admin_iframe'), lecturer_form)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTrue(Lecturer.objects.filter(
            username='test_fe_lecturer').exists())

        student_form = {
            'username': 'test_fe_student',
            'first_name': 'Test_fe_student',
            'last_name': 'Test_fe_student',
            'email': 'test_fe_student@test.com',
            'matr_nr': '42069',
            'password': '12345'
        }
        response = self.client.post(
            reverse('createstudent_admin_iframe'), student_form)
        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertTrue(Student.objects.filter(
            username='test_fe_student').exists())

        # create a course to do stuff with in the test
        c = Course(
            name='test_course_fe',
            start_date='2021-08-08',
            end_date='2021-10-10'
        )

        c.lecturer = Lecturer.objects.get(username='test_fe_lecturer')
        c.save()
        c.student.add(Student.objects.get(username='test_fe_student'))
        c.save()
        self.assertTrue(Course.objects.filter(name='test_course_fe').exists())

        # create an exercise to do stuff with in the tests
        e = Exercise(
            description='420 lodern Sie es!',
            start_time='2021-08-08 14:00:00',
            work_time_duration=parse_duration('0 days 00:10:00'),
            submission_deadline='2021-08-08 15:15:00',
        )
        e.course = Course.objects.get(name='test_course_fe')
        e.save()
        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())

    def test_deny_anonymous_view_fileexchange(self):
        """
        Basically tests if the '@login_required' works/is set up everywhere
        """
        self.client.logout()

        response = self.client.get(reverse('overview'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(self.client.get(reverse('overview')),
                             '/accounts/login/?next=/file_exchange/overview/')

        response = self.client.get(reverse('create_exersice'), {})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            self.client.get(
                reverse('create_exersice'),
                {}),
            '/accounts/login/?next=/file_exchange/exercises/create/')

        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.get(reverse('deleted_exersice', kwargs={
                                   'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            self.client.get(
                reverse(
                    'deleted_exersice',
                    kwargs={
                        'id': my_id})),
            '/accounts/login/?next=/file_exchange/exercises/delete/1')

        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.get(reverse('alter_exersice', kwargs={
                                   'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(self.client.get(reverse('alter_exersice', kwargs={
            'id': my_id})),
            '/accounts/login/?next=/file_exchange/exercises/alter/1')

    def test_overview_view(self):
        self.client.force_login(self.my_admin)

        response = self.client.get(reverse('overview'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_exercise_view(self):
        self.client.force_login(self.my_admin)

        response = self.client.post(reverse('create_exersice'), {
            'description': 'Testexercise woohoo!',
            'start_time_0': '2021-08-08',
            'start_time_1': '08:00',
            'work_time_duration': '0 00:10:00',
            'submission_deadline_0': '2021-08-08',
            'submission_deadline_1': '09:15',
            'course': Course.objects.get(name='test_course_fe').id
        })
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Exercise.objects.filter(
            description='Testexercise woohoo!').exists())

    def test_delete_exercise_view(self):
        self.client.force_login(self.my_admin)

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.post(
            reverse('deleted_exersice', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())

    def test_delete_exercise_view_as_lecturer(self):
        self.client.force_login(
            Lecturer.objects.get(username='test_fe_lecturer'))

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.post(
            reverse('deleted_exersice', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())

    def test_alter_exercise_view(self):
        self.client.force_login(self.my_admin)

        exercise_form = {
            'description': 'Testexercise woohoo!',
            'start_time_0': '2021-08-08',
            'start_time_1': '08:00',
            'work_time_duration': '0 00:10:00',
            'submission_deadline_0': '2021-08-08',
            'submission_deadline_1': '09:15',
            'course': Course.objects.get(name='test_course_fe').id
        }

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.get(
            reverse('alter_exersice', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(
            reverse('alter_exersice', kwargs={'id': my_id}), exercise_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Exercise.objects.get(
                id=my_id).description == 'Testexercise woohoo!')

    def test_alter_exercise_view_as_lecturer(self):
        self.client.force_login(
            Lecturer.objects.get(
                username='test_fe_lecturer'))

        exercise_form = {
            'description': 'Testexercise woohoo!',
            'start_time_0': '2021-08-08',
            'start_time_1': '08:00',
            'work_time_duration': '0 00:10:00',
            'submission_deadline_0': '2021-08-08',
            'submission_deadline_1': '09:15',
            'course': Course.objects.get(name='test_course_fe').id
        }

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.get(
            reverse('alter_exersice', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(
            reverse('alter_exersice', kwargs={'id': my_id}), exercise_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            Exercise.objects.get(
                id=my_id).description == 'Testexercise woohoo!')

    def test_upload_file_view(self):
        self.client.force_login(self.my_admin)

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.post(
            reverse('upload', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_download_file_view(self):
        self.client.force_login(self.my_admin)

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.post(
            reverse('download', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_exercise_site_view(self):
        self.client.force_login(self.my_admin)

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.post(
            reverse('exersice_site', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_exercise_site_view_as_lecturer(self):
        self.client.force_login(
            Lecturer.objects.get(
                username='test_fe_lecturer'))

        self.assertTrue(Exercise.objects.filter(
            description='420 lodern Sie es!').exists())
        my_id = Exercise.objects.get(description='420 lodern Sie es!').id
        response = self.client.post(
            reverse('exersice_site', kwargs={'id': my_id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_filename_view(self):
        self.assertEqual(
            filename('upload/course_1/exercise_1/compilerbau_2019.pdf'),
            'compilerbau_2019.pdf')

        self.assertEqual(
            filename(
                'upload/course_132113/exercise_1444444/_compilerbau_2019_harald.pdf'),
            '_compilerbau_2019_harald.pdf')
