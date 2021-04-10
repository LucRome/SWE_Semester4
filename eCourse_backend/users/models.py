from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    This class represents the different types of users.
    The three different groups of users are:

    - student
    - lecturer
    - administrator/superuser
    - staff

    The class is derived from django's AbstracUser. Hence it only additionally needs the matr_nr field.
    """
    matr_nr = models.IntegerField(default=0)
    


class Lecturer(User):
    class Meta:
        proxy = True
        permissions = [('alter_courses', 'Can alter course')]

class Student(User):
    class Meta:
        proxy = True
        
class Office(User):
    class Meta:
        proxy = True
        permissions = [('alter_courses', 'Can alter course'),
                        ('create_courses', 'Can create course'),
                        ('delete_courses', 'Can delete course'),
                        ('manage_users', 'Can manage user'),]
    