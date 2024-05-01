from django.urls import path
from .views import CurrencyRateListView

urlpatterns = [
    path('currencyRatesPerCurrency', CurrencyRateListView.as_view(), name='currency-rate-per-currency'),
]
