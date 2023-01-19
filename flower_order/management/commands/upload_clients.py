import json

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from flower_order.models import Client


class Command(BaseCommand):
    help = 'Start adding clients'

    def handle(self, *args, **options):

        with open(options['path'], 'r', encoding='utf-8') as file:
            clients = json.load(file)

        for client in clients:
            self.add_client(client)

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            nargs='?',
            type=str,
        )

    def add_client(self, client_notes: dict):
        try:
            client, created = Client.objects.get_or_create(
                phonenumber=client_notes['phonenumber'],
                defaults={
                    'name': client_notes.get('name', ''),
                    'surname': client_notes.get('surname', ''),
                }
            )

        except IntegrityError:
            client = f"{client_notes.get('surname', '')} {client_notes.get('name', '')}"
            created = False

        if created:
            self.stdout.write(f'Created client "{client}".')
        else:
            self.stdout.write(f'\033[93mDOUBLE:\033[0m client "{client}" already exists!')
