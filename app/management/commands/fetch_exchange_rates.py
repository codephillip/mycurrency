from django.core.management.base import BaseCommand
from app.models import Currency, CurrencyExchangeRate
from datetime import datetime

from app.services.provider_service import MockProvider, get_exchange_rate_data
from mycurrency.constants import DATE_FORMAT, FETCH_HELP, DATE_FORMAT_ERROR, DATE_HELP, RATES_FETCHED_SUCCESS


class Command(BaseCommand):
    help = FETCH_HELP

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help=DATE_HELP, required=False)

    def handle(self, *args, **options):
        date_str = options.get('date')
        if date_str:
            try:
                valuation_date = datetime.strptime(date_str, DATE_FORMAT)
            except ValueError:
                self.stdout.write(self.style.ERROR(DATE_FORMAT_ERROR))
                return
        else:
            valuation_date = datetime.now()

        currencies = Currency.objects.all()
        provider = MockProvider(url='mock_url', apikey='mock_apikey')

        for source_currency in currencies:
            for exchanged_currency in currencies:
                if exchanged_currency != source_currency:
                    rates = get_exchange_rate_data(source_currency.code, exchanged_currency.code, valuation_date,
                                                   provider)
                    if rates:
                        exchange_rate = CurrencyExchangeRate(
                            source_currency=source_currency,
                            exchanged_currency=exchanged_currency,
                            valuation_date=valuation_date,
                            rate_value=rates[exchanged_currency.code]
                        )
                        exchange_rate.save()
        self.stdout.write(self.style.SUCCESS(RATES_FETCHED_SUCCESS))
