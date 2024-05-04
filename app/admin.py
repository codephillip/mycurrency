from django.contrib import admin

from app.models import Currency, CurrencyExchangeRate, ProviderModel
from django.urls import path
from django.shortcuts import render
from app.forms import CurrencyExchangeForm
from django.http import HttpRequest
from app.views import CurrencyConverterView

admin.site.register(Currency)
admin.site.register(ProviderModel)


class CurrencyExchangeAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('currencyExchange/', self.currency_exchange_view),
        ]
        return custom_urls + urls

    def currency_exchange_view(self, request):
        if request.method == 'POST':
            form = CurrencyExchangeForm(request.POST)
            if form.is_valid():
                source_currency = form.cleaned_data['source_currency']
                exchanged_currencies = form.cleaned_data['exchanged_currencies']
                amount = form.cleaned_data['amount']
                result = dict()

                for currency in exchanged_currencies.split(','):
                    params = {
                        'source_currency': source_currency,
                        'amount': amount,
                        'exchanged_currency': currency
                    }
                    request = HttpRequest()
                    request.method = 'GET'
                    request.GET = params
                    response = CurrencyConverterView.as_view()(request)
                    res = response.data
                    result[currency] = res['data']['exchanged_amount']
                return render(request, 'currency_exchange_result.html', {'result': result})
        else:
            form = CurrencyExchangeForm()
        return render(request, 'currency_exchange_form.html', {'form': form})


admin.site.register(CurrencyExchangeRate, CurrencyExchangeAdmin)
