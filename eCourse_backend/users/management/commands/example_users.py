import random
import os
import csv
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

__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)))
DIR = os.path.join(__location__, 'data_names')


def read_surenames():
    file = os.path.join(DIR, 'surenames.txt')
    with open(file) as f:
        content = [x.strip() for x in f]
    return content


def read_prenames():
    file = os.path.join(DIR, 'prenames.csv')
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        content = [lines[0] for lines in csv_reader]
    return content


class Command(BaseCommand):
    help = 'Create ' + \
        str(USER_NUM) + ' random users that can be used to test the application'

    def handle(self, *args, **options):
        first_names = read_prenames()
        last_names = read_surenames()
        for i in USER_NUM:
            t = (i % 3) + 1
            first = random.sample(first_names, 1)[0]
            last = random.sample(last_names, 1)[0]
            if t == 1:
                user_name = 'Verwaltungsangestellter' + str(i)
            elif t == 2:
                user_name = 'Dozent' + str(i)
            elif t == 3:
                user_name = 'Studierender' + str(i)
            # user_name = str(random.randint(10000,90000))
            u = User(
                username=user_name,
                first_name=first,
                last_name=last,
                email=user_name + '@example.com',
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
