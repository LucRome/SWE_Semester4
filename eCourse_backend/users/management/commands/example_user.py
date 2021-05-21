import string
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from users.models import User


def rand_word(l):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(l))


class Command(BaseCommand):
    help = 'Create 20 random users that can be used to test the application'
    u1 = User(
        username='Verwaltungsangestellter1',
        first_name='Daniel',
        last_name='Goldschmidt',
        email='d.goldschmidt@example.com',
        matr_nr=0,
        type=1)
    u2 = User(
        username='Verwaltungsangestellter2',
        first_name='Julia',
        last_name='Unger',
        email='j.unger@example.com',
        matr_nr=0,
        type=1)
    u3 = User(
        username='Verwaltungsangestellter3',
        first_name='Florian',
        last_name='Foerster',
        email='f.foerstert@example.com',
        matr_nr=0,
        type=1)
    u4 = User(
        username='Dozent1',
        first_name='Mathias',
        last_name='Faber',
        email='m.faber@example.com',
        matr_nr=0,
        type=2)
    u5 = User(
        username='Dozent2',
        first_name='Lukas',
        last_name='Schultheiss',
        email='l.schultheiss@example.com',
        matr_nr=0,
        type=2)
    u6 = User(
        username='Dozent3',
        first_name='Ursula',
        last_name='Drescher',
        email='u.drescher@example.com',
        matr_nr=0,
        type=2)
    u7 = User(
        username='Dozent4',
        first_name='Janina',
        last_name='Dresner',
        email='j.dresner@example.com',
        matr_nr=0,
        type=2)
    u8 = User(
        username='Student1',
        first_name='David',
        last_name='Maurer',
        email='d.maurer@example.com',
        matr_nr=1659,
        type=3)
    u9 = User(
        username='Student2',
        first_name='Jens',
        last_name='Furst',
        email='j.furst@example.com',
        matr_nr=3753,
        type=3)
    u10 = User(
        username='Student3',
        first_name='Erik',
        last_name='Muller',
        email='e.muller@example.com',
        matr_nr=7076,
        type=3)
    u11 = User(
        username='Student4',
        first_name='Andrea',
        last_name='Hoch',
        email='a.hochr@example.com',
        matr_nr=9094,
        type=3)
    u12 = User(
        username='Student5',
        first_name='Ines',
        last_name='Maur',
        email='i.maur@example.com',
        matr_nr=1922,
        type=3)
    u13 = User(
        username='Student6',
        first_name='Antje',
        last_name='Kunze',
        email='a.kunze@example.com',
        matr_nr=7492,
        type=3)

    def handle(self, *args, **options):
        users = [self.u1, self.u2, self.u3, self.u4, self.u5, self.u6, self.u7,
                 self.u8, self.u9, self.u10, self.u11, self.u12, self.u13]
        for i in range(0, 12):
            users[i].set_password('test123')
            users[i].save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully created testuser of type {} with username: {}'.format(
                        users[i].type,
                        users[i].username)))
