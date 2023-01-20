from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView
from .models import Bouquet, Category, Shop
import re


class BouquetListView(ListView):
    model = Bouquet
    queryset = Bouquet.objects.all()[:3]
    context_object_name = 'bouquets'
    template_name = "flower_order/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['shops'] = Shop.objects.all()
        return context


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

    def get_context_data(self, **kwargs):
        self.template_name = "flower_order/order-step.html"
        context = super().get_context_data(**kwargs)
        if self.request.GET:
            first_name = self.request.GET.get('fname', '')
            tel = self.request.GET.get('tel', '')
            address = self.request.GET.get('address', '')
            pattern = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')
            if not bool(pattern.findall(tel)):
                self.template_name = "flower_order/order.html"

            # Добавить еще логики
        return context


class Quiz(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = "flower_order/quiz.html"


class QuizStep(TemplateView):
    template_name = "flower_order/quiz-step.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class Result(ListView):
    template_name = "flower_order/result.html"
    context_object_name = 'bouquet'

    def get_queryset(self):
        if self.request.GET:
            event, min_price, max_price = self.request.GET.get('event', '').split('_')
            category = get_object_or_404(Category, title=event)
            return category.bouquets.filter(
                price__gt=int(min_price),
                price__lte=int(max_price)
            ).order_by('?').first()


class Card(TemplateView):
    template_name = "flower_order/card.html"
