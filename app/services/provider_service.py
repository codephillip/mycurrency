import sys
from importlib import import_module
from typing import List
from abc import ABC, abstractmethod

from app.models import ProviderModel


class Provider(ABC):
    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey

    @abstractmethod
    def execute_api(self, source_currency, exchanged_currencies, valuation_date):
        pass

    @abstractmethod
    def get_exchange_rate_data(self, source_currency: str, exchanged_currencies: List[str], valuation_date: str):
        pass


def get_exchange_rate_data(source_currency: str, exchanged_currencies: List[str], valuation_date: str):
    providers = ProviderModel.objects.order_by('priority')

    for model in providers:
        sys.path.append(model.module_dir)
        converter_module = import_module(model.module_name)
        result = converter_module.provider.get_exchange_rate_data(source_currency, exchanged_currencies, valuation_date)
        if result:
            return result
    return None