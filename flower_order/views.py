from django.views.generic import ListView
from .models import Bouquet


class BouquetListView(ListView):
    model = Bouquet
    context_object_name = 'bouquets'
    template_name = "flower_order/test.html"

