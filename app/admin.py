from django.contrib import admin

from app.models import Currency, CurrencyExchangeRate, ProviderModel, CURRENCY_CHOICES
from django.urls import path
from django.shortcuts import render
from app.forms import CurrencyExchangeForm
from django.http import HttpRequest
from app.views import CurrencyConverterView


class CurrencyExchangeAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('currencyExchange/', self.currency_exchange_view),
            path('exchangeRateGraph/', self.exchange_rate_graph_view),
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

    def exchange_rate_graph_view(self, request):
        exchange_data = {}
        currency_rates = CurrencyExchangeRate.objects.all().order_by('valuation_date')
        for currency_rate in currency_rates:
            key = f'{currency_rate.source_currency}/{currency_rate.exchanged_currency}'
            if key not in exchange_data:
                exchange_data[key] = []
            exchange_data[key].append(float(currency_rate.rate_value))

        distinct_dates = CurrencyExchangeRate.objects.values('valuation_date').distinct().order_by('valuation_date')
        exchange_data['dates'] = [date['valuation_date'].strftime('%Y-%m-%d') for date in distinct_dates]
        return render(request, 'exchange_rate_graph.html', {'data': exchange_data})


admin.site.register(Currency)
admin.site.register(ProviderModel)
admin.site.register(CurrencyExchangeRate, CurrencyExchangeAdmin)
