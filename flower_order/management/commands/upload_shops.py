import json

from django.core.management.base import BaseCommand

from flower_order.models import Shop


class Command(BaseCommand):
    help = 'Start adding shops'

    def handle(self, *args, **options):

        with open(options['path'], 'r', encoding='utf-8') as file:
            shops = json.load(file)

        for shop in shops:
            self.add_shop(shop)

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            nargs='?',
            type=str,
        )

    def add_shop(self, restaurant_notes: dict):
        shop, created = Shop.objects.get_or_create(
            phonenumber=restaurant_notes['phonenumber'],
            defaults={
                'address': restaurant_notes.get('address', ''),
                'image': restaurant_notes.get('image', None),
                'latitude': restaurant_notes.get('latitude', 55.775076),
                'longitude': restaurant_notes.get('longitude', 37.720429),

            }
        )

        if created:
            self.stdout.write(f'Added shop "{shop}".')
        else:
            self.stdout.write(f'\033[93mDOUBLE:\033[0m shop "{shop}" already exists!')
