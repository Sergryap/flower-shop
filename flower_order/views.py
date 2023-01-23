from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView, DetailView, RedirectView
from .models import Bouquet, Category, Shop, Client, Order
from django.db.models import Window, F
from django.db.models.functions import DenseRank, Random
import re


class ConsultationSendMixin:

    @staticmethod
    def verify_phone(tel):
        pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')
        return bool(pattern.findall(tel))

    @staticmethod
    def normalize_phone(tel):
        return ''.join(['+7'] + [i for i in tel if i.isdigit()][-10:])

    def save_order_consultation(self):
        if self.request.GET:
            tel = self.request.GET.get('tel', '')
            if self.verify_phone(tel):
                first_name = self.request.GET.get('fname', '')
                tel = self.normalize_phone(tel)
                client, __ = Client.objects.get_or_create(phonenumber=tel, defaults={'name': first_name})
                Order.objects.create(client=client, service='consultation', comment='Заявка на консультацию')


class BouquetListView(ListView, ConsultationSendMixin):
    model = Bouquet
    queryset = Bouquet.objects.annotate(number=Window(expression=DenseRank(), order_by=[Random()]))[:3]
    context_object_name = 'bouquets'
    template_name = "flower_order/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        self.save_order_consultation()
        return context


class CatalogListView(ListView, ConsultationSendMixin):
    model = Bouquet
    context_object_name = 'blocks'
    template_name = "flower_order/catalog.html"

    def get_queryset(self):
        item, blocks = [], []
        if self.request.GET.get('display') == 'more':
            bouquets = Bouquet.objects.annotate(number=Window(expression=DenseRank(), order_by=[F('pk').desc()]))
            all_row = len(bouquets) // 3
        else:
            bouquets = Bouquet.objects.annotate(number=Window(expression=DenseRank(), order_by=[Random()]))
            all_row = 2
        row_number = 0
        for bouquet in bouquets:
            item.append(bouquet)
            if bouquet.number % 3 == 0:
                blocks.append(item)
                item = []
                row_number += 1
            if row_number == all_row:
                break
        blocks.append(item)
        return blocks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.save_order_consultation()
        if self.request.GET.get('display') == 'more':
            context['display'] = '1'
            context['button_text'] = 'Скрыть'
            context['block_name'] = 'Все букеты'
        else:
            context['display'] = 'more'
            context['button_text'] = 'Показать всё'
            context['block_name'] = 'Примеры букетов'
        return context


class Consultation(TemplateView, ConsultationSendMixin):
    template_name = "flower_order/consultation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.save_order_consultation()
        return context


class OrderView(TemplateView, ConsultationSendMixin):
    template_name = "flower_order/order.html"

    def get_context_data(self, **kwargs):
        bouquet_pk = self.request.GET.get('bouquet', 0)
        context = super().get_context_data(**kwargs)
        context['bouquet_pk'] = bouquet_pk
        context['delivery_times'] = [
            'Как можно скорее',
            'с 10:00 до 12:00',
            'с 12:00 до 14:00',
            'с 14:00 до 16:00',
            'с 16:00 до 18:00',
            'с 18:00 до 20:00'
        ]
        self.save_order_consultation()

        if bouquet_pk and int(bouquet_pk):
            bouquet = Bouquet.objects.get(pk=bouquet_pk)
            context['price'] = f'{bouquet.price} ₽'

        return context


class OrderStep(TemplateView, ConsultationSendMixin):

    def get_context_data(self, **kwargs):
        self.template_name = "flower_order/order-step.html"
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            tel = self.request.GET.get('tel', '')
            if not self.verify_phone(tel):
                self.template_name = "flower_order/order.html"
            else:
                first_name = self.request.GET.get('fname', '')
                address = self.request.GET.get('address', '')
                bouquet_pk = self.request.GET.get('bouquet', '0')
                order_time = self.request.GET.get('orderTime', '')
                tel = self.normalize_phone(tel)
                client, __ = Client.objects.get_or_create(phonenumber=tel, defaults={'name': first_name})
                order = Order.objects.create(client=client, address=address, comment=order_time, service='delivery')
                if bouquet_pk and int(bouquet_pk):
                    bouquet = Bouquet.objects.get(pk=bouquet_pk)
                    order.bouquets.add(bouquet)
                    context['price'] = f'{bouquet.price} ₽'
        # блок оплаты
        if self.request.GET.get('price', ''):
            self.template_name = "flower_order/order-step.html"
            card_num = self.request.GET.get('cardNum', '')
            card_month = self.request.GET.get('cardMm', '')
            card_year = self.request.GET.get('cardGg', '')
            card_name = self.request.GET.get('cardFname', '')
            card_cvc = self.request.GET.get('cardCvc', '')
            card_mail = self.request.GET.get('mail', '')
            price = int(self.request.GET.get('price', 0))
            print(card_name, card_month, card_year, card_cvc, price)
            #payment_send(payment_bot=settings.BOT, value=round(price, 0), chat_id=os.environ['TELEGRAM_ID']) #тестовая оплата через бота
        return context


class Quiz(ListView, ConsultationSendMixin):
    model = Category
    context_object_name = 'categories'
    template_name = "flower_order/quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.save_order_consultation()
        return context


class QuizStep(TemplateView, ConsultationSendMixin):
    template_name = "flower_order/quiz-step.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.save_order_consultation()
        event = self.request.GET.get('event', '')
        category = get_object_or_404(Category, title=event)
        context['event'] = event
        price_range = list(category.bouquets.order_by('price'))
        max_price = round(price_range[-1].price, 0)
        min_price = round(price_range[0].price, 0)
        prices = [
            {'min': '0', 'max': f'{min_price + 100}', 'text': f'До {min_price + 100} руб'},
            {'min': f'{min_price + 100}', 'max': f'{max_price - 100}', 'text': f'{min_price + 100} - {max_price - 100} руб'},
            {'min': f'{max_price - 100}', 'max': 1000000, 'text': f'От {max_price - 100}'},
            {'min': 0, 'max': 1000000, 'text': 'Не имеет значения'}
        ]
        context['prices'] = prices
        return context


class Result(ListView, ConsultationSendMixin):
    template_name = "flower_order/result.html"
    context_object_name = 'bouquet'

    def get_queryset(self):
        self.save_order_consultation()
        if self.request.GET:
            event, min_price, max_price = self.request.GET.get('event', '').split('_')
            category = get_object_or_404(Category, title=event)
            return category.bouquets.filter(
                price__gt=int(min_price),
                price__lte=int(max_price)
            ).order_by('?').first()


class Card(DetailView, ConsultationSendMixin):
    template_name = "flower_order/card.html"
    model = Bouquet
    context_object_name = 'bouquet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.save_order_consultation()
        return context


class OrderStepRedirectView(RedirectView, ConsultationSendMixin):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        tel = self.request.GET.get('tel', '')

        if not self.verify_phone(tel):
            self.url = self.request.META.get('HTTP_REFERER')
            return super().get_redirect_url(*args, **kwargs)
        else:
            first_name = self.request.GET.get('fname', '')
            address = self.request.GET.get('address', '')
            bouquet_pk = self.request.GET.get('bouquet', '0')
            order_time = self.request.GET.get('orderTime', '')
            tel = self.normalize_phone(tel)
            client, __ = Client.objects.get_or_create(phonenumber=tel, defaults={'name': first_name})
            order = Order.objects.create(client=client, address=address, comment=order_time, service='delivery')

            if bouquet_pk and int(bouquet_pk):
                bouquet = Bouquet.objects.get(pk=bouquet_pk)
                order.bouquets.add(bouquet)

        return super().get_redirect_url(*args, **kwargs)
