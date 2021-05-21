import random
import string
from datetime import date
from django.core.management.base import BaseCommand, CommandError
from users.models import Lecturer, Student, User
from courses.models import Course

COURSE_NUM = range(5)

course_names = [
    '19IN-Rechnerarchitekturen',
    '19IN-Compilerbau',
    '19IN-Web Engineering',
    '19IN-Betriebssysteme',
    '19IN-SWE',
    '19IN-Signale und Systeme',
    '19IN-Statistik',
    '19IN-Matlab',
    '19IN-Wahlfach',
    '19IN-Elektrotechnik',
    '19IN-Physik',
    '19IN-ETST']


def rand_word(len):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(len))


def db_to_list(type):
    elm = User.objects.filter(type=type)
    res = []
    if elm:
        for e in elm:
            res.append(e.id)
    return res


def calc_start_date():
    start_dt = date.today().replace(day=1, month=1).toordinal()
    end_dt = date.today().toordinal()
    return date.fromordinal(random.randint(start_dt, end_dt))


def calc_end_date():
    start_dt = date.today().toordinal()
    end_dt = date.today().replace(year=(date.today().year + 1)).toordinal()
    return date.fromordinal(random.randint(start_dt, end_dt))


def rand_num_students(students):
    n = random.randint(1, len(students))
    return random.sample(students, n)


class Command(BaseCommand):
    help = 'Create 5 random courses with already created users as students and lecturers'

    def handle(self, *args, **options):
        lec = db_to_list(2)
        stud = db_to_list(3)
        for i in COURSE_NUM:
            # random names:
            # c.name = rand_word(12)
            # some real course names
            # c.name = random.sample(course_names, 1)[0]
            # c.save()
            c = Course(
                name=rand_word(11),
                start_date=calc_start_date(),
                end_date=calc_end_date()
            )

            try:
                c.lecturer = Lecturer.objects.get(id=random.sample(lec, 1)[0])
                c.save()
                list_student_ids = rand_num_students(stud)
                for j in range(0, len(list_student_ids)):
                    c.student.add(Student.objects.get(id=list_student_ids[j]))
                    c.save()
            except BaseException:
                raise CommandError('Could not create course')

            self.stdout.write(
                self.style.SUCCESS(
                    'Successfully created testcourse with name {}'.format(
                        c.name)))
