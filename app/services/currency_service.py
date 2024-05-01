from collections import defaultdict

from app.models import CurrencyExchangeRate


def convert_currency(source_currency: str, amount: float, exchanged_currency: str):
    try:
        exchange_rate = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency.upper(),
            exchanged_currency__code=exchanged_currency.upper()
        ).latest('valuation_date')
    except CurrencyExchangeRate.DoesNotExist:
        return None

    exchanged_amount = amount * exchange_rate.rate_value
    return exchanged_amount, exchange_rate.rate_value

def currency_converter_response(source_currency, amount, exchanged_currency):
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


def get_currency_exchanges(date_from, date_to, source_currency):
    currency_exchanges = CurrencyExchangeRate.objects.filter(
        valuation_date__range=(date_from, date_to),
        source_currency__code=source_currency
    ).select_related('exchanged_currency')

    response_data = defaultdict(list)
    for currency_exchange in currency_exchanges:
        currency_code = currency_exchange.exchanged_currency.code
        response_data[currency_code].append({
            'date': str(currency_exchange.valuation_date),
            'value': float(currency_exchange.rate_value)
        })
    return response_data
