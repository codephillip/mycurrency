from datetime import datetime, timedelta
from decimal import Decimal

from app.models import CurrencyExchangeRate
from app.services.currency_service import get_rate_value
from mycurrency.constants import DATE_FORMAT


def generate_datetime_range(start_datetime: datetime, end_datetime: datetime):
    return [start_datetime + i * timedelta(days=1) for i in range((end_datetime - start_datetime).days)]


def calculate_twrr(source_currency: str, amount: float, exchanged_currency: str, start_date: datetime,
                   end_date=datetime.now()):
    exchanges = CurrencyExchangeRate.objects.filter(
        valuation_date__range=(start_date, end_date),
        source_currency__code=source_currency,
        exchanged_currency__code=exchanged_currency
    ).order_by('valuation_date')

    if not exchanges.exists():
        exchanges = []
        for valuation_date in generate_datetime_range(start_date, end_date):
            rate_value = get_rate_value(source_currency, exchanged_currency, valuation_date)
            if rate_value:
                exchanges.append(rate_value)

    if not exchanges:
        return []

    twrrs = []
    start_value = exchanges[0].rate_value * amount
    for index, exchange in enumerate(exchanges):
        if index:
            twrrs.append({
                "valuation_date": exchange.valuation_date.strftime(DATE_FORMAT),
                "source_twrr": round(twrr_formula(amount, start_value / exchange.rate_value, index + 1) * 100, 1),
                "exchanged_twrr": round(twrr_formula(start_value, amount * exchange.rate_value, index + 1) * 100, 1)
            })
    return twrrs


def twrr_formula(start_value: float, end_value: float, n: int) -> Decimal:
    if not start_value:
        return Decimal(0)
    return ((Decimal(end_value) / Decimal(start_value)) ** Decimal(1 / n)) - 1
