from django.contrib import admin

from app.models import Currency, CurrencyExchangeRate

admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
