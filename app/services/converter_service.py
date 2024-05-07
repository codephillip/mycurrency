from decimal import Decimal

from app.services.currency_service import get_rate_value


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
