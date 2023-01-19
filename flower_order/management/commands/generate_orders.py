import random

from django.core.management.base import BaseCommand

from flower_order.models import Bouquet, Client, Order, Staff


class Command(BaseCommand):
    help = 'Start adding staffs'

    def handle(self, *args, **options):
        self.generate_orders()

    def generate_orders(self):
        bouquets = Bouquet.objects.all()
        clients = Client.objects.all()
        staff_couriers = Staff.objects.filter(position='courier')
        staff_masters = Staff.objects.filter(position='master')
        addreses = [
            'Москва, ул. Ленина, д. 60, кв 10',
            'Москва, ул. Петина, д. 6, кв 300',
            'Москва, ул. Иванова, д. 16, кв 80',
            'Москва, ул. Петрова, д. 26, кв 8',
            'Москва, ул. Юрова, д. 15, кв 6',
        ]

        # Created consultations
        consultation_num = random.randint(1, len(clients))
        for client in random.choices(clients, k=consultation_num):
            order_consultation = Order.objects.create(
                client=client,
                service='consultation',
                staff=random.choice(staff_masters),
            )
            self.stdout.write(f'Created order "{order_consultation}".')

        # Created delivery
        delivery_num = random.randint(1, len(clients))
        for client in random.choices(clients, k=delivery_num):
            order_delivery = Order.objects.create(
                client=client,
                service='delivery',
                staff=random.choice(staff_couriers),
                address=random.choice(addreses),
            )

            bouquet_num = random.randint(1, len(bouquets))
            order_bouquets = random.choices(bouquets, k=bouquet_num)

            for bouquet in order_bouquets:
                order_delivery.bouquets.add(bouquet)

            order_delivery.save()

            self.stdout.write(f'Created order "{order_delivery}".')
