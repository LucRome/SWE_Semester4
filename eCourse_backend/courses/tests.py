from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from django.db import IntegrityError

from django.core.management import call_command

from users.models import Student
from users.models import Lecturer
from .models import *
from .views import *

# Create your tests here.


class CoursesTestCase(TestCase):

    def setUp(self):
        call_command('loadperms', 'groups.yml')
        self.my_admin = User.objects.create_superuser(
            'admin', 'admin@admin.com', 'admin123')

    def test_courses_without_login(self):
        self.client.logout()

        response = self.client.get('/courses/delete', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/courses/overview/page', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/courses/create', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get('/courses/edit', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_course_form(self):
        s = Student(
            username='testilon2',
            first_name='Testvorname4',
            last_name='Testnachname4',
            email='test4@test.com'
        )
        s.save()
        l = Lecturer(
            username='testilon',
            first_name='Testvorname3',
            last_name='Testnachname3',
            email='test3@test.com'
        )
        l.save()

        course_form = {
            'lecturer': l.id,
            'start_date': '2021-06-09',
            'end_date': '2023-06-09',
            'student': [s.id],
            'name': 'TestCourse'
        }
        course = CourseForm(course_form)
        self.assertTrue(course.is_valid())
        course.save()

    def test_create_and_delete_course_view(self):
        self.client.force_login(self.my_admin)
        s = Student(
            username='testilon2',
            first_name='Testvorname4',
            last_name='Testnachname4',
            email='test4@test.com'
        )
        s.save()
        l = Lecturer(
            username='testilon',
            first_name='Testvorname3',
            last_name='Testnachname3',
            email='test3@test.com'
        )
        l.save()

        course_form = {
            'lecturer': l.id,
            'start_date': '2021-06-09',
            'end_date': '2023-06-09',
            'student': [s.id],
            'name': 'TestCourse'
        }

        course_form2 = {
            'lecturer': l.id,
            'start_date': '2021-06-09',
            'end_date': '2023-06-09',
            'student': [s.id],
            'name': 'ChangedCourse'
        }

        response = self.client.post(
            reverse('create_course'), course_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        query_set = Course.objects.all()
        self.assertTrue(Course.objects.filter(name='TestCourse').exists())
        my_id = Course.objects.get(name='TestCourse').id

        response = self.client.post(
            reverse('edit_course', kwargs={'id': my_id}), course_form2)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Course.objects.filter(name='ChangedCourse').exists())

        response = self.client.post(
            reverse('detailed_course', args=(my_id,)))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        """
        response = self.client.post(
            reverse('course_overview', kwargs={'page': 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        """
        response = self.client.post(
            reverse('delte_course', args=(my_id,)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        query_set = Course.objects.all()
        self.assertFalse(Course.objects.filter(name='TestCourse').exists())
