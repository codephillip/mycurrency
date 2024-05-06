import random
import sys
from importlib import import_module
from typing import List
from abc import ABC, abstractmethod

from app.models import ProviderModel
from datetime import datetime


class Provider(ABC):
    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey

    @abstractmethod
    def execute_api(self, source_currency, exchanged_currencies, valuation_date):
        pass

    @abstractmethod
    def get_exchange_rate_data(self, source_currency: str, exchanged_currencies: List[str],
                               valuation_date: datetime) -> dict:
        pass


class MockProvider(Provider):
    def execute_api(self, source_currency, exchanged_currencies, valuation_date):
        pass

    def get_exchange_rate_data(self, source_currency: str, exchanged_currencies: List[str], valuation_date: datetime):
        return {currency: round(random.uniform(0.5, 1.1), 6) for currency in exchanged_currencies}


def transform_to_executable(provider_model: ProviderModel):
    sys.path.append(provider_model.module_dir)
    return import_module(provider_model.module_name).provider


def get_exchange_rate_data(source_currency: str, exchanged_currency: str, valuation_date: datetime,
                           provider: Provider):
    rates = provider.get_exchange_rate_data(source_currency, [exchanged_currency], valuation_date)
    if rates:
        return rates

    providers = ProviderModel.objects.all()
    for model in providers:
        provider = transform_to_executable(model)
        rates = provider.get_exchange_rate_data(source_currency, [exchanged_currency], valuation_date)
        if rates:
            return rates
    return None
