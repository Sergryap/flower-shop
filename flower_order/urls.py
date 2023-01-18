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
    path('', BouquetListView.as_view(), name='start'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('consultation/', Consultation.as_view(), name='consultation'),
    path('order/', Order.as_view(), name='order'),
    path('order-step/', OrderStep.as_view(), name='order_step'),
    path('quiz/', Quiz.as_view(), name='quiz'),
    path('result/', Result.as_view()),
    path('card/', Card.as_view()),
]
