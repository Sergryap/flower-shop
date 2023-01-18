from django.urls import path

from .views import BouquetListView


app_name = "flower_order"

urlpatterns = [
    path('test/', BouquetListView.as_view()),
]
