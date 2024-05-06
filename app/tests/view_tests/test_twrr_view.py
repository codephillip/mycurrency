from decimal import Decimal

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

        self.date_to = datetime.strptime('2024-05-07 11:00', '%Y-%m-%d %H:%M')

        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=self.date_to - timedelta(days=3),
            rate_value=1.5
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=self.date_to - timedelta(days=2),
            rate_value=1.8
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=self.date_to - timedelta(days=1),
            rate_value=1.2
        )
        CurrencyExchangeRate.objects.create(
            source_currency=dollar,
            exchanged_currency=euro,
            valuation_date=self.date_to,
            rate_value=1.35
        )

        data = {
            'source_currency': 'USD',
            'amount': 100,
            'exchanged_currency': 'EUR',
            'start_date': (self.date_to - timedelta(days=3)).strftime('%Y-%m-%d'),
            'end_date': self.date_to.strftime('%Y-%m-%d')
        }

        url = reverse('calculate-twrr')
        response = self.client.get(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('data', response.data)
        self.assertEqual(len(response.data['data']), 3)
        self.assertEqual(response.data['data'], [
            {'valuation_date': '2024-05-05', 'source_twrr': Decimal('-8.7'), 'exchanged_twrr': Decimal('9.5')},
            {'valuation_date': '2024-05-06', 'source_twrr': Decimal('7.7'), 'exchanged_twrr': Decimal('-7.2')},
            {'valuation_date': '2024-05-07', 'source_twrr': Decimal('2.7'), 'exchanged_twrr': Decimal('-2.6')}])

    def test_invalid_start_date_input_parameters(self):
        url = reverse('calculate-twrr')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        data = {
            'source_currency': 'USD',
            'amount': 100,
            'exchanged_currency': 'EUR',
            'start_date': '2024/01/01',
            'end_date': '2024/01/04'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('start_date', response.data)
        self.assertIn('end_date', response.data)

    def test_no_historical_exchange_rate_data(self):
        url = reverse('calculate-twrr')
        data = {
            'source_currency': 'USD',
            'amount': 100,
            'exchanged_currency': 'EUR',
            'start_date': '2250-01-01',
            'end_date': '2250-01-05'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['data']), 0)

    def test_end_data_less_than_start_data(self):
        url = reverse('calculate-twrr')
        data = {
            'source_currency': 'USD',
            'amount': 100,
            'exchanged_currency': 'EUR',
            'start_date': '2250-01-01',
            'end_date': '2000-01-05'
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('End date must be greater than start date', response.data['end_date'])

    def test_invalid_input_amount_parameters(self):
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
