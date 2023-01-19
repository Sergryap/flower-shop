import json

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from flower_order.models import Staff


class Command(BaseCommand):
    help = 'Start adding staffs'

    def handle(self, *args, **options):

        with open(options['path'], 'r', encoding='utf-8') as file:
            staffs = json.load(file)

        for staff in staffs:
            self.add_staff(staff)

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            nargs='?',
            type=str,
        )

    def add_staff(self, staff_notes: dict):
        try:
            staff, created = Staff.objects.get_or_create(
                phonenumber=staff_notes['phonenumber'],
                position=staff_notes['position'],
                defaults={
                    'name': staff_notes.get('name', ''),
                    'surname': staff_notes.get('surname', ''),
                }
            )

        except IntegrityError:
            staff = f"{staff_notes['position']}:{staff_notes.get('surname', '')} {staff_notes.get('name', '')}"
            created = False

        if created:
            self.stdout.write(f'Created staff "{staff}".')
        else:
            self.stdout.write(f'\033[93mDOUBLE:\033[0m staff "{staff}" already exists!')
