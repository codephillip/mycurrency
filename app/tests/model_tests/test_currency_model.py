from django.db import IntegrityError
from django.test import TestCase
from app.models import Currency
from django.core.exceptions import ValidationError


class CurrencyModelTest(TestCase):
    def setUp(self):
        Currency.objects.create(code='USD', name='US Dollar', symbol='$')

    def test_right_currency_code_value_returned(self):
        currency = Currency.objects.get(code='USD')
        self.assertEqual(currency.code, 'USD')

    def test_create_currency_for_duplicate_code(self):
        with self.assertRaises(IntegrityError):
            Currency.objects.create(code='USD', name='Another US Dollar', symbol='US$')

    def test_create_currency_for_invalid_code(self):
        with self.assertRaises(ValidationError):
            Currency.objects.create(code='XYZ', name='Another XYZ', symbol='US$')

    def test_currency_creation_with_lowercase(self):
        currency = Currency.objects.create(code='eur', name='Euro', symbol='€')
        self.assertEqual(currency.code, 'EUR')

    def test_protected_currency_deletion(self):
        with self.assertRaises(ValidationError):
            currency = Currency.objects.create(code='eur', name='Euro', symbol='€', is_protected=True)
            currency.delete()

    def test_unprotected_currency_deletion(self):
        currency = Currency.objects.create(code='eur', name='Euro', symbol='€', is_protected=False)
        currency.delete()
