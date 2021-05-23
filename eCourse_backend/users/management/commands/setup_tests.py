from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):
        call_command('flush', interactive=False)
        call_command('migrate')
        call_command('loadperms', 'groups.yml')
        call_command('create_testusers')
        call_command('frontend_tests')
