from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_save
from django.dispatch import receiver 
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

    class Meta:
        permissions = [('manage_users', 'Manages Users')]


class Lecturer(User):
    objects = LecturerManager()

    class Meta:
        proxy = True

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

    def save(self, *args, **kwargs):
        self.type = 1
        return super(Office, self).save(*args, **kwargs)

@receiver(post_save, sender=Office)
@receiver(post_save, sender=Student)
@receiver(post_save, sender=Lecturer)
@receiver(post_save, sender=User)
def add_user_to_public_group(sender, instance, created, **kwargs):
    """Post-create user signal that adds the user to everyone group."""
    if created:
        t = instance.type
        instance.groups.add(Group.objects.get(pk=t))
