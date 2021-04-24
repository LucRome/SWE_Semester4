from django.contrib.auth.models import UserManager


class OfficeManager(UserManager):
    def get_queryset(self):
        return super(OfficeManager, self).get_queryset().filter(type=1)


class LecturerManager(UserManager):
    def get_queryset(self):
        return super(LecturerManager, self).get_queryset().filter(type=2)


class StudentManager(UserManager):
    def get_queryset(self):
        return super(StudentManager, self).get_queryset().filter(type=3)
