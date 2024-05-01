from django.test import TestCase
from app.models import Currency, CurrencyExchangeRate
from datetime import date
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class CurrencyExchangeRateModelTest(TestCase):
    def setUp(self):
        Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        Currency.objects.create(code='EUR', name='Euro', symbol='€')

        self.exchange_rate = CurrencyExchangeRate.objects.create(
            source_currency=Currency.objects.get(code='USD'),
            exchanged_currency=Currency.objects.get(code='EUR'),
            valuation_date=date(2024, 1, 1),
            rate_value=1.2
        )

    def test_exchange_rate_retrieval(self):
        exchange_rate = CurrencyExchangeRate.objects.get(valuation_date=date(2024, 1, 1),
                                                         source_currency=Currency.objects.get(code='USD'),
                                                         exchanged_currency=Currency.objects.get(code='EUR'))
        self.assertEqual(exchange_rate.source_currency.code, 'USD')
        self.assertEqual(exchange_rate.exchanged_currency.code, 'EUR')

    def test_exchange_not_found_with_wrong_currency(self):
        with self.assertRaises(ObjectDoesNotExist):
            CurrencyExchangeRate.objects.get(valuation_date=date(2024, 1, 1),
                                             source_currency=Currency.objects.get(code='USD'),
                                             exchanged_currency=Currency.objects.get(code='XYZ'))

    def test_exchange_not_found_for_validation_date(self):
        with self.assertRaises(ObjectDoesNotExist):
            CurrencyExchangeRate.objects.get(valuation_date=date(2023, 1, 1),
                                             source_currency=Currency.objects.get(code='USD'),
                                             exchanged_currency=Currency.objects.get(code='EUR'))

    def test_create_exchange_currency_with_same_currency_fails(self):
        with self.assertRaises(ValidationError):
            CurrencyExchangeRate.objects.create(
                source_currency=Currency.objects.get(code='USD'),
                exchanged_currency=Currency.objects.get(code='USD'),
                valuation_date=date(2024, 1, 1),
                rate_value=1.2
            )
