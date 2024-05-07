from collections import defaultdict
from datetime import datetime

from app.models import CurrencyExchangeRate


def get_currency_exchanges(date_from: datetime, date_to: datetime, source_currency: str):
    currency_exchanges = CurrencyExchangeRate.objects.filter(
        valuation_date__range=(date_from, date_to),
        source_currency__code=source_currency
    ).select_related('exchanged_currency').order_by('valuation_date')

    response_data = defaultdict(list)
    for currency_exchange in currency_exchanges:
        currency_code = currency_exchange.exchanged_currency.code
        response_data[currency_code].append({
            'date': str(currency_exchange.valuation_date),
            'value': float(currency_exchange.rate_value)
        })
    return response_data
