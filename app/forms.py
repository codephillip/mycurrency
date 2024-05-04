from django import forms
from django.core.validators import RegexValidator


class CurrencyExchangeForm(forms.Form):
    source_currency = forms.CharField(max_length=3)
    exchanged_currencies = forms.CharField(
        max_length=800,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{3}(,\s*[A-Z]{3})*$',
                message='Enter comma-separated currencies in three-letter format eg USD, GBP'
            )
        ]
    )
    amount = forms.DecimalField(decimal_places=6, max_digits=18)
