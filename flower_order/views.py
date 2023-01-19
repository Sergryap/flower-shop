from pprint import pprint

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View, DetailView, TemplateView
from django.views.generic.detail import TemplateResponseMixin
from django.views.generic.list import BaseListView, MultipleObjectTemplateResponseMixin, ContextMixin
from .models import Bouquet, Category


class BouquetListView(ListView):
    model = Bouquet
    queryset = Bouquet.objects.all()[:3]
    context_object_name = 'bouquets'
    template_name = "flower_order/index.html"


class CatalogListView(ListView):
    model = Bouquet
    queryset = Bouquet.objects.all()
    context_object_name = 'bouquets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # item_quantity = Bouquet.objects.count()
        # if self.request.resolver_match.url_name == 'catalog':
        context['block1'] = Bouquet.objects.all()[:3]
        context['block2'] = Bouquet.objects.all()[3:6]
        return context

    template_name = "flower_order/catalog.html"


class Consultation(TemplateView):
    template_name = "flower_order/consultation.html"


class Order(TemplateView):
    template_name = "flower_order/order.html"


class OrderStep(TemplateView):
    template_name = "flower_order/order-step.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            first_name = self.request.GET.get('fname', '')
            tel = self.request.GET.get('tel', '')
            address = self.request.GET.get('address', '')

            # Добавить еще логики
        return context


class Quiz(TemplateView):
    template_name = "flower_order/quiz.html"


class QuizStep(TemplateView):
    template_name = "flower_order/quiz-step.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('marriage'):
            context['event'] = 'marriage'
        elif self.request.GET.get('birthday'):
            context['event'] = 'birthday'
        else:
            context['event'] = 'empty'
        return context


class Result(ListView):
    template_name = "flower_order/result.html"
    context_object_name = 'bouquets'

    def get_queryset(self):
        if self.request.GET:
            event, price = self.request.GET.get('event', '').split('_')
            category_name = {'empty': 'Без повода', 'marriage': 'Свадьба', 'birthday': 'День рождения'}
            price_value = {'1': (0, 1000), '2': (1000, 5000), '3': (5000, 1000000), '4': (0, 1000000)}
            category = get_object_or_404(Category, title=category_name[event])
            return category.bouquets.all().filter(
                price__gt=price_value[price][0],
                price__lte=price_value[price][1]
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            event, price = self.request.GET.get('event', '').split('_')
            context['event'] = event  # Эти переменные можно использовать для шаблона
            context['price'] = price
            print(event, price)
        return context


class Card(TemplateView):
    template_name = "flower_order/card.html"
