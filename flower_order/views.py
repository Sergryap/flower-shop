from django.views.generic import ListView, View, DetailView
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


class Consultation(ListView):
    model = Bouquet
    template_name = "flower_order/consultation.html"
