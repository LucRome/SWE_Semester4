from django.test import TestCase
from .views import filename

#help function for filename see views.py
class TestFun(TestCase):
    def test0(self):
        self.assertEqual(filename('upload/course_1/exercise_1/compilerbau_2019.pdf'), 'compilerbau_2019.pdf')
    def test1(self):
        self.assertEqual(filename('upload/course_132113/exercise_1444444/_compilerbau_2019_harald.pdf'), '_compilerbau_2019_harald.pdf')


# Create your tests here.
