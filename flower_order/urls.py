from django.urls import path

from .views import (
    BouquetListView,
    CatalogListView,
    Consultation,
    Order,
    OrderStep,
    Quiz,
    Result,
    Card
)


app_name = "flower_order"

urlpatterns = [
    path('', BouquetListView.as_view()),
    path('catalog/', CatalogListView.as_view()),
    path('consultation/', Consultation.as_view()),
    path('order/', Order.as_view()),
    path('order-step/', OrderStep.as_view()),
    path('quiz/', Quiz.as_view()),
    path('result/', Result.as_view()),
    path('card/', Card.as_view()),
]
