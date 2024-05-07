from collections import defaultdict
from decimal import Decimal

from app.models import CurrencyExchangeRate, ProviderModel
from datetime import datetime, timedelta

from app.services.provider_service import get_exchange_rate_data, transform_to_executable
from mycurrency.constants import DATE_FORMAT


def get_exchange_from_server(source_currency: str, exchanged_currency: str, valuation_date=datetime.now()):
    try:
        provider = transform_to_executable(ProviderModel.objects.first())
        rates = get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider)
        rate_value = rates[exchanged_currency]
        return rate_value
    except Exception as e:
        print(e)
    return None


def get_rate_value(source_currency: str, exchanged_currency: str, valuation_date=datetime.now()):
    try:
        exchange_rate = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency.upper(),
            exchanged_currency__code=exchanged_currency.upper()
        ).latest('valuation_date')
        if exchange_rate:
            return exchange_rate.rate_value
        exchange_rate = CurrencyExchangeRate.objects.filter(
            source_currency__code=exchanged_currency.upper(),
            exchanged_currency__code=source_currency.upper()
        ).latest('valuation_date')
        if exchange_rate:
            return 1 / exchange_rate.rate_value
    except Exception as e:
        print(e)
    return get_exchange_from_server(source_currency, exchanged_currency, valuation_date)


def convert_currency(source_currency: str, amount: float, exchanged_currency: str):
    rate_value = get_rate_value(source_currency, exchanged_currency)

    if not rate_value:
        return None
    exchanged_amount = Decimal(amount) * Decimal(rate_value)
    return exchanged_amount, rate_value


def format_currency_converter_response(source_currency: str, amount: float, exchanged_currency: str):
    result = convert_currency(source_currency, amount, exchanged_currency)
    if result:
        exchanged_amount, exchange_rate = result
        return {
            'source_currency': source_currency,
            'amount': amount,
            'exchanged_currency': exchanged_currency,
            'exchanged_amount': exchanged_amount,
            'exchange_rate': exchange_rate
        }
    return None


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
