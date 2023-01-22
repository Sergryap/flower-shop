from django.urls import path

from .views import (
    BouquetListView,
    CatalogListView,
    Consultation,
    OrderView,
    OrderStep,
    Quiz,
    QuizStep,
    Result,
    Card,
    OrderStepRedirectView,
)


app_name = "flower_order"
payment_url = 'https://api.paybox.money/payment.php?pg_merchant_id=526740&pg_amount=200&pg_currency=RUB&pg_description=Футболка+с+принтом&pg_salt=kFQ4pYsAV1K531C0&pg_sig=26c83d710e86e916acffb80ea931a30e'

urlpatterns = [
    path('', BouquetListView.as_view(), name='start'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('catalog/all/', CatalogListView.as_view(), name='all_catalog'),
    path('consultation/', Consultation.as_view(), name='consultation'),
    path('order/', OrderView.as_view(), name='order'),
    # path('order-step/', OrderStep.as_view(), name='order_step'),
    path('order-step/', OrderStepRedirectView.as_view(url=payment_url), name='order_step'),
    path('quiz/', Quiz.as_view(), name='quiz'),
    path('quiz-step/', QuizStep.as_view(), name='quiz_step'),
    path('result/', Result.as_view(), name='result'),
    path('card/<int:pk>/', Card.as_view(), name='card'),
]
