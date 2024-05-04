from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime, timedelta

from app.models import Currency, CurrencyExchangeRate


class TWRRViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_calculate_twrr_success(self):
        dollar = Currency.objects.create(code='USD', name='US Dollar', symbol='$')
        euro = Currency.objects.create(code='EUR', name='Euro', symbol='€')

        self.date_from = datetime.now().date() - timedelta(days=2)
        self.date_to = datetime.now()

        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=datetime.now().date() - timedelta(days=2),
            rate_value=0.85
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=datetime.now().date() - timedelta(days=1),
            rate_value=0.90
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=datetime.now().date(),
            rate_value=0.95
        )
        data = {
            'source_currency': 'USD',
            'amount': 100,
            'exchanged_currency': 'EUR',
            'start_date': self.date_from.strftime('%Y-%m-%d')
        }

        url = reverse('calculate-twrr')
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)

    def test_invalid_start_date_input_parameters(self):
        url = reverse('calculate-twrr')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        data = {
            'source_currency': 'USD',
            'amount': 100,
            'exchanged_currency': 'EUR',
            'start_date': '2024/01/01'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('start_date', response.data)

    def test_no_historical_exchange_rate_data(self):
        url = reverse('calculate-twrr')
        data = {
            'source_currency': 'USD',
            'amount': 100,
            'exchanged_currency': 'EUR',
            'start_date': '2250-01-01'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)

    def test_valid_input_amount_parameters(self):
        url = reverse('calculate-twrr')
        start_date = datetime(2024, 1, 1)
        data = {
            'source_currency': 'USD',
            'amount': 'one hundred',
            'exchanged_currency': 'EUR',
            'start_date': start_date.strftime('%Y-%m-%d')
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('amount', response.data)
