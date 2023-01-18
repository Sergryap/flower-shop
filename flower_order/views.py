from django.views.generic import ListView, View, DetailView, TemplateView
from django.views.generic.detail import TemplateResponseMixin
from django.views.generic.list import BaseListView, MultipleObjectTemplateResponseMixin, ContextMixin
from .models import Bouquet


class BouquetListView(ListView):
    model = Bouquet
    context_object_name = 'bouquets'
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
    template_name = "flower_order/order-step.html"


class Quiz(TemplateView):
    template_name = "flower_order/quiz.html"


class Result(TemplateView):
    template_name = "flower_order/result.html"


class Card(TemplateView):
    template_name = "flower_order/card.html"
