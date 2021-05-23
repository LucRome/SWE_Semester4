import string
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from users.models import User


class Command(BaseCommand):
    help = 'Create Users and courses frontend tests depend on'
    u1 = User(
        username='KATRIN',
        first_name='hilfe',
        last_name='why',
        email='ich@will.de',
        matr_nr=10000,
        type=1,
    )
    u2 = User(
        username='mholtzmann',
        first_name='hilfe',
        last_name='why',
        email='ich@willnicht.de',
        matr_nr=111,
        type=1,
    )
    u3 = User(
        username='hilfmir',
        first_name='nein',
        last_name='nochmalnein',
        email='maa@dhbw.de',
        matr_nr=165423121222,
        type=2,
    )
    u4 = User(
        username='mabt',
        first_name='hilfe',
        last_name='whynot',
        email='holfe@dhbw.de',
        matr_nr=1111551,
        type=2,
    )
    u5 = User(
        username='mbaier',
        first_name='Mandy',
        last_name='Baier',
        email='mbaier@dhbw.de',
        matr_nr=690815,
        type=3,
    )
    u6 = User(
        username='yeisenberg',
        first_name='hilfe',
        last_name='mehrhilfe',
        email='maxhilfe@dhbw.de',
        matr_nr=1551111,
        type=3,
    )
    u7 = User(
        username='kpfaff',
        first_name='Karolin',
        last_name='Pfaff',
        email='kpfaff@dhbw.de',
        matr_nr=0,
        type=1,
    )

    def handle(self, *args, **options):
        users = [self.u1, self.u2, self.u3, self.u4, self.u5, self.u6, self.u7]

        for user in users:
            user.set_password('admin123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Created user with username: {} and password: {}'.format(
                        user.username,
                        user.password)))
