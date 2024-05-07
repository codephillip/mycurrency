from django.test import TestCase
from app.services.twrr_service import twrr_formula


class TestTWRR(TestCase):
    def test_twrr_formula(self):
        self.assertEqual(0.02669, float(round(twrr_formula(10000, 11111.1111, 4), 5)))

    def test_same_value(self):
        self.assertEqual(0, float(round(twrr_formula(10000, 10000, 1), 5)))

    def test_zero_division_error(self):
        self.assertEqual(0, float(round(twrr_formula(0, 0, 1), 5)))




