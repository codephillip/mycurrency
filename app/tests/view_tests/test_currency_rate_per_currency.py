from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime, timedelta

from app.models import CurrencyExchangeRate, Currency


class CurrencyRatePerCurrencyTests(TestCase):
    def setUp(self):
        dollar = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        euro = Currency.objects.create(code='EUR', name='Euro', symbol='€')
        gbp = Currency.objects.create(code='GBP', name='Pound', symbol='ERE')

        self.date_from = datetime.now().date()
        self.date_to = self.date_from + timedelta(days=1)

        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=self.date_from,
            rate_value=0.85
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=self.date_to,
            rate_value=0.91
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=gbp,
            valuation_date=self.date_from,
            rate_value=1.73
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=gbp,
            valuation_date=self.date_to,
            rate_value=1.75
        )
        self.client = APIClient()

    def test_get_currency_rate_per_currency_success(self):
        source_currency = 'USD'

        url = reverse('currency-rate-per-currency')
        response = self.client.get(url,
                                   {'date_from': self.date_from,
                                    'date_to': self.date_to,
                                    'source_currency': source_currency})

        self.assertEqual(response.status_code, 200)

        expected_data = {
            'data': {
                'source': source_currency,
                'exchanges': {
                    'EUR': [
                        {'date': str(self.date_from), 'value': 0.85},
                        {'date': str(self.date_to), 'value': 0.91},
                    ],
                    'GBP': [
                        {'date': str(self.date_from), 'value': 1.73},
                        {'date': str(self.date_to), 'value': 1.75}
                    ]
                }
            }
        }
        self.assertEqual(response.data, expected_data)

    def test_invalid_date_format(self):
        url = reverse('currency-rate-per-currency')
        response = self.client.get(url, {'date_from': '2022/05/01', 'date_to': '2022/05/05', 'source_currency': 'USD'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('Date has wrong format. Use one of these formats instead: YYYY-MM-DD.',
                      response.data['date_from'])
        self.assertIn('Date has wrong format. Use one of these formats instead: YYYY-MM-DD.', response.data['date_to'])

    def test_date_from_after_date_to(self):
        url = reverse('currency-rate-per-currency')
        response = self.client.get(url, {'date_from': '2024-05-05', 'date_to': '2024-05-01', 'source_currency': 'USD'})

        self.assertEqual(response.status_code, 400)
        self.assertIn('date_from must be before date_to', response.data['non_field_errors'])
