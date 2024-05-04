from django.core.management.base import BaseCommand
from app.models import Currency, CurrencyExchangeRate
from datetime import datetime

from app.services.provider_service import MockProvider, get_exchange_rate_data
from mycurrency.constants import DATE_FORMAT


class Command(BaseCommand):
    help = 'Fetch exchange rates once a day and save them in CurrencyExchangeRate'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='Date in the format YYYY-MM-DD (optional)', required=False)

    def handle(self, *args, **options):
        date_str = options.get('date')
        if date_str:
            try:
                valuation_date = datetime.strptime(date_str, DATE_FORMAT)
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid date format. Please use YYYY-MM-DD'))
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
                            rate_value=rates
                        )
                        exchange_rate.save()
                        print(exchange_rate)
        self.stdout.write(self.style.SUCCESS('Exchange rates fetched and saved successfully'))
