from app.models import CurrencyExchangeRate

def currency_converter(source_currency: str, amount: float, exchanged_currency: str):
    try:
        exchange_rate = CurrencyExchangeRate.objects.filter(
            source_currency__code=source_currency.upper(),
            exchanged_currency__code=exchanged_currency.upper()
        ).latest('valuation_date')
    except CurrencyExchangeRate.DoesNotExist:
        return None

    exchanged_amount = amount * exchange_rate.rate_value
    return exchanged_amount, exchange_rate.rate_value
