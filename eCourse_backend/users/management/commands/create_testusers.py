import random
import string
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from users.models import User

USER_NUM = range(20)

USER_GROUPS = [
    'office_users',
    'lecturer_users',
    'student_users',
]


def rand_word(l):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(l))


class Command(BaseCommand):
    help = 'Create 20 random users that can be used to test the application'

    def handle(self, *args, **options):
        for i in USER_NUM:
            t = (i % 3) + 1
            u = User(
                username=rand_word(10),
                first_name=rand_word(9),
                last_name=rand_word(10),
                email=rand_word(10) + '@example.com',
                matr_nr=random.randint(10000, 9999999),
                type=t,
            )
            try:
                u.set_password('test123')
                u.save()
            except Exception:
                raise CommandError('Could not create user')

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully created testuser of type {} with username: {}'.format(
                        t, u.username)))