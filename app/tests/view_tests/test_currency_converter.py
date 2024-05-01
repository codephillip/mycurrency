from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from app.models import CurrencyExchangeRate, Currency


class CurrencyConverterTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.usd = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        self.eur = Currency.objects.create(code='EUR', name='Euro', symbol='€')

        CurrencyExchangeRate.objects.create(
            source_currency=self.usd,
            exchanged_currency=self.eur,
            valuation_date=datetime.now(),
            rate_value=0.85
        )
        CurrencyExchangeRate.objects.create(
            source_currency=self.usd,
            exchanged_currency=self.eur,
            valuation_date=datetime.now() - timedelta(days=1),
            rate_value=0.82
        )

    def test_currency_converter_success(self):
        url = reverse('currency-converter')
        response = self.client.get(url, {
            'source_currency': 'USD',
            'amount': '100',
            'exchanged_currency': 'EUR'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('source_currency', str(response.data))
        self.assertIn('amount', str(response.data))
        self.assertIn('exchanged_currency', str(response.data))
        self.assertIn('exchanged_amount', str(response.data))
        self.assertIn('exchange_rate', str(response.data))
        self.assertEqual(85.0, response.data['data']['exchanged_amount'])

    def test_currency_with_lowercase(self):
        url = reverse('currency-converter')
        response = self.client.get(url, {
            'source_currency': 'usd',
            'amount': '100',
            'exchanged_currency': 'EUR'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('source_currency', str(response.data))
        self.assertEqual(85.0, response.data['data']['exchanged_amount'])
        self.assertEqual('USD', response.data['data']['source_currency'])
        self.assertEqual('EUR', response.data['data']['exchanged_currency'])

    def test_invalid_amount(self):
        url = reverse('currency-converter')
        response = self.client.get(url, {
            'source_currency': 'USD',
            'amount': 'invalid',
            'exchanged_currency': 'EUR'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('amount', response.data)

    def test_missing_params(self):
        url = reverse('currency-converter')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 400)
        error_details = response.data.get('source_currency')
        self.assertIsNotNone(error_details)
        self.assertIn('This field is required.', str(error_details))
        self.assertIn('amount', response.data)
        self.assertIn('exchanged_currency', response.data)

    def test_rate_not_found(self):
        url = reverse('currency-converter')
        response = self.client.get(url, {
            'source_currency': 'USD',
            'amount': '100',
            'exchanged_currency': 'XYZ'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', str(response.data))

    def test_same_source_and_exchanged_currency(self):
        url = reverse('currency-converter')
        response = self.client.get(url, {
            'source_currency': 'USD',
            'amount': '100',
            'exchanged_currency': 'USD'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', str(response.data))
