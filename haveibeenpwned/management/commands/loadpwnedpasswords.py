import os

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from haveibeenpwned.models import  PwnedPassword


class Command(BaseCommand):
    help = 'Load pwned passwords to database'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        filename = options['filepath']
        if not os.path.isfile(filename):
            raise CommandError('File does not exists')

        with open(filename) as f:
            self.stdout.write('Processing file %s' % (filename))
            for number, line in enumerate(f, 1):
                try:
                    PwnedPassword.objects.create(
                        hash=line.strip()
                    )
                except IntegrityError:
                    pass
                self.stdout.write('Hashes loaded: %d \r' % (number), ending='')
                self.stdout.flush()

        self.stdout.write('Hashes loaded: %d \r' % (number))
