from django.views.generic import ListView, View, DetailView, TemplateView
from django.views.generic.detail import TemplateResponseMixin
from django.views.generic.list import BaseListView, MultipleObjectTemplateResponseMixin, ContextMixin
from .models import Bouquet


class BouquetListView(ListView):
    model = Bouquet
    queryset = Bouquet.objects.all()[:3]
    context_object_name = 'bouquets' # Переменная, которая попадает в шаблон
    template_name = "flower_order/index.html"


class CatalogListView(ListView):
    model = Bouquet
    context_object_name = 'bouquets'
    template_name = "flower_order/catalog.html"


class Consultation(TemplateView):
    template_name = "flower_order/consultation.html"


class Order(TemplateView):
    template_name = "flower_order/order.html"


class OrderStep(TemplateView):
    def get(self, request, *args, **kwargs):
        context = super().get(request, *args, **kwargs)
        if self.request.GET:
            print(self.request.GET)
            context['delivery_data'] = self.request.GET
            # Добавить еще логики
        return context
    template_name = "flower_order/order-step.html"


class Quiz(TemplateView):
    template_name = "flower_order/quiz.html"


class Result(TemplateView):
    template_name = "flower_order/result.html"


class Card(TemplateView):
    template_name = "flower_order/card.html"
