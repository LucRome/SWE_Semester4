from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import *

# Create your models here.

USER_TYPES = [
    (1, 'Office'),
    (2, 'Lecturer'),
    (3, 'Student'),
]


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
    type = models.IntegerField(choices=USER_TYPES, default=3)
    matr_nr = models.IntegerField(default=0)


class Lecturer(User):
    objects = LecturerManager()

    class Meta:
        proxy = True
        permissions = [('alter_courses', 'Can alter course'),
                       ('create_exercise', 'Can create exercises')]

    def save(self, *args, **kwargs):
        self.type = 2
        return super(Lecturer, self).save(*args, **kwargs)


class Student(User):
    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.type = 3
        return super(Student, self).save(*args, **kwargs)


class Office(User):
    objects = OfficeManager()

    class Meta:
        proxy = True
        permissions = [('alter_courses', 'Can alter course'),
                       ('create_courses', 'Can create course'),
                       ('delete_courses', 'Can delete course'),
                       ('manage_users', 'Can manage user'),
                       ('create_exercise', 'Can create exercises'),
                      ]

    def save(self, *args, **kwargs):
        self.type = 1
        return super(Office, self).save(*args, **kwargs)