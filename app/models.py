from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

USD = 'USD'
EUR = 'EUR'
CHF = 'CHF'
GBP = 'GBP'

CURRENCY_CHOICES = [
    (USD, 'US Dollar'),
    (EUR, 'Euro'),
    (CHF, 'Swiss Franc'),
    (GBP, 'British Pound Sterling'),
]


class Currency(models.Model):
    code = models.CharField(max_length=3, choices=CURRENCY_CHOICES, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)
    is_protected = models.BooleanField(default=True)

    def __str__(self):
        return self.code

    def delete(self, *args, **kwargs):
        if self.is_protected:
            raise ValidationError('This currency is protected and cannot be deleted.')
        super().delete(*args, **kwargs)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.code:
            self.code = self.code.upper()
        if self.code not in [choice[0] for choice in CURRENCY_CHOICES]:
            raise ValidationError('Currency not accepted')
        super().save(force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency,
                                        related_name='exchanges',
                                        on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency,
                                           on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.source_currency.code == self.exchanged_currency.code:
            raise ValidationError('Source and exchanged currency must be different')
        super().save(force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)


class ProviderModel(models.Model):
    name = models.CharField(max_length=20, unique=True)
    priority = models.IntegerField(blank=False, null=False, default=100)
    module_dir = models.CharField(max_length=300)
    module_name = models.CharField(max_length=300, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['priority', 'created_at']
