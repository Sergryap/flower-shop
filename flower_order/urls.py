from django.urls import path

from .views import BouquetListView, CatalogListView, Consultation


app_name = "flower_order"

urlpatterns = [
    path('', BouquetListView.as_view()),
    path('catalog/', CatalogListView.as_view()),
    path('consultation/', Consultation.as_view())
]
