from django.urls import path
from .views import CurrencyRatePerCurrencyView, CurrencyConverterView, TWRRView, UploadExchangesJson

urlpatterns = [
    path('currencyRatesPerCurrency', CurrencyRatePerCurrencyView.as_view(), name='currency-rate-per-currency'),
    path('currencyConverter', CurrencyConverterView.as_view(), name='currency-converter'),
    path('calculateTWRR', TWRRView.as_view(), name='calculate-twrr'),
    path('uploadExchangesJson', UploadExchangesJson.as_view(), name='upload-exchanges-json'),
]
