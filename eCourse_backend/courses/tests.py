from django.test import TestCase
from http import HTTPStatus
from django.urls import reverse
from django.db import IntegrityError

from django.core.management import call_command
import logging

from .models import *
from .views import *

# Create your tests here.
class CoursesTestCase(TestCase):
    def setUp(self):
        call_command('loadperms', 'groups.yml')
        self.my_admin = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
        self.logger = logging.getLogger('django.db.backends')

        """
        user_form = {
            'username': 'testilon',
            'first_name': 'Testvorname3',
            'last_name': 'Testnachname3',
            'email': 'test3@test.com',
            'type': 'Lecturer'
        }
        
        response = self.client.post(
            reverse('createlecturer_admin_iframe'), user_form)
        """
    def test_courses_without_login(self):
        self.client.logout();

        response = self.client.get('/courses/delete', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/courses/overview/page', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

        response = self.client.get('/courses/create', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get('/courses/edit', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_course_form(self):
        course_form = {
            'lecturer': 'testilon',
            'start_date': '2021-06-09',
            'end_date': '2023-06-09',
            'student': 2,
            'id': 5,
            'lecturer_id': 6,
            'name': 'TestCourse',
            'exercise': ''
        }
        course = CourseForm(course_form)
        course.is_valid()
        """
        self.logger.error('course.errors')
        #self.assertTrue()
        """
        #self.assertTrue(course.is_valid())
        course.save()
        
    
    def test_create_course_view(self):
        self.client.force_login(self.my_admin)
        course_form = {
            'Lecturer': 'testilon',
            'start_date': '10.12.2010',
            'end_date': '10.12.2012',
            'name': 'TestCourse'
        }
        
        response = self.client.post(
            reverse('create_course'), course_form)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        query_set = Course.objects.all()
        self.assertTrue(Course.objects.filter(name='TestCourse').exists())
