from django.contrib import admin

from app.models import Currency, CurrencyExchangeRate, ProviderModel

admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
admin.site.register(ProviderModel)
