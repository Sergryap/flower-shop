from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView
from .models import Bouquet, Category, Shop, Client, Order
from django.db.models import Window, F
from django.db.models.functions import DenseRank
import re


class ConsultationSendMixin:

    @staticmethod
    def phone_verify(tel):
        pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')
        return bool(pattern.findall(tel))

    def consultation_send(self):
        if self.request.GET:
            tel = self.request.GET.get('tel', '')
            if self.phone_verify(tel):
                first_name = self.request.GET.get('fname', '')
                tel = ''.join(['+7'] + [i for i in tel if i.isdigit()][-10:])
                Client.objects.get_or_create(phonenumber=tel, defaults={'name': first_name})


class BouquetListView(ListView, ConsultationSendMixin):
    model = Bouquet
    queryset = Bouquet.objects.all()[:3]
    context_object_name = 'bouquets'
    template_name = "flower_order/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        self.consultation_send()
        return context


class CatalogListView(ListView, ConsultationSendMixin):
    model = Bouquet
    queryset = Bouquet.objects.all()
    template_name = "flower_order/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bouquets = Bouquet.objects.annotate(number=Window(expression=DenseRank(), order_by=[F('pk').desc()]))
        item, blocks = [], []
        self.consultation_send()
        if self.request.GET.get('display') == 'more':
            all_row = len(bouquets) // 3
            context['display'] = '1'
            context['button_text'] = 'Скрыть'
            context['block_name'] = 'Все букеты'
        else:
            all_row = 1
            context['display'] = 'more'
            context['button_text'] = 'Показать ещё'
            context['block_name'] = 'Примеры букетов'
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
        context['blocks'] = blocks
        return context


class Consultation(TemplateView, ConsultationSendMixin):
    template_name = "flower_order/consultation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.consultation_send()
        return context


class OrderView(TemplateView, ConsultationSendMixin):
    template_name = "flower_order/order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bouquet_pk'] = self.request.GET.get('bouquet', 0)
        self.consultation_send()
        return context


class OrderStep(TemplateView, ConsultationSendMixin):

    def get_context_data(self, **kwargs):
        self.template_name = "flower_order/order-step.html"
        context = super().get_context_data(**kwargs)
        self.consultation_send()
        if self.request.GET:
            tel = self.request.GET.get('tel', '')
            if not self.phone_verify(tel):
                self.template_name = "flower_order/order.html"
            else:
                first_name = self.request.GET.get('fname', '')
                address = self.request.GET.get('address', '')
                bouquet_pk = self.request.GET.get('bouquet', '0')
                order_time = self.request.GET.get('orderTime', '')
                tel = ''.join(['+7'] + [i for i in tel if i.isdigit()][-10:])
                client, __ = Client.objects.get_or_create(phonenumber=tel, defaults={'name': first_name})
                order = Order.objects.create(client=client, address=address, comment=order_time)
                if bouquet_pk and int(bouquet_pk):
                    bouquet = Bouquet.objects.get(pk=bouquet_pk)
                    order.bouquets.add(bouquet)
        return context


class Quiz(ListView, ConsultationSendMixin):
    model = Category
    context_object_name = 'categories'
    template_name = "flower_order/quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.consultation_send()
        return context


class QuizStep(TemplateView, ConsultationSendMixin):
    template_name = "flower_order/quiz-step.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.consultation_send()
        event = self.request.GET.get('event', '')
        category = get_object_or_404(Category, title=event)
        context['event'] = event
        max_price = round(category.bouquets.order_by('-price').first().price, 0)
        min_price = round(category.bouquets.order_by('price').first().price, 0)
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
        self.consultation_send()
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
        self.consultation_send()
        return context

