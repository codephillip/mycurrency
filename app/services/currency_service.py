from unsync import unsync
from app.models import CurrencyExchangeRate, ProviderModel, Currency
from datetime import datetime

from app.services.provider_service import get_exchange_rate_data, transform_to_executable


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


@unsync
def save_exchanges_async(base_currency, date, rates_data):
    """
    Sqlite as db will have multiple locks, consider doing it synchronously
    """
    for currency_code, rate_value in rates_data.items():
        source_currency = Currency.objects.get(code=base_currency)
        exchanged_currency = Currency.objects.get(code=currency_code)
        CurrencyExchangeRate.objects.update_or_create(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=date,
            defaults={'rate_value': rate_value}
        )
