import json

from django.core.management.base import BaseCommand

from flower_order.models import Bouquet, Category


class Command(BaseCommand):
    help = 'Start adding bouquets'

    def handle(self, *args, **options):

        with open(options['path'], 'r', encoding='utf-8') as file:
            bouquets = json.load(file)

        for bouquet in bouquets:
            self.add_bouquet(bouquet)

    def add_arguments(self, parser):
        parser.add_argument(
            'path',
            nargs='?',
            type=str,
        )

    def add_bouquet(self, bouquet_notes: dict):
        bouquet_obj, bouquet_created = Bouquet.objects.get_or_create(
            title=bouquet_notes['title'],
            price=bouquet_notes['price'],
            image=bouquet_notes['image'],
            defaults={
                'structure': bouquet_notes.get('structure', ''),
                'height': bouquet_notes.get('height', 50),
                'width': bouquet_notes.get('width', 20),
            }
        )
        print(bouquet_obj, bouquet_created)
        for category in bouquet_notes.get('categories', ['Без повода']):
            print(category)
            category_obj, category_created = Category.objects.get_or_create(title=category)
            bouquet_obj.categories.add(category_obj)

        if bouquet_created:
            self.stdout.write(f'Added bouquet "{bouquet_obj}".')
        else:
            self.stdout.write(f'\033[93mDOUBLE:\033[0m bouquet "{bouquet_obj}" already exists!')
