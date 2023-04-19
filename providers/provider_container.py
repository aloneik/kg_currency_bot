from typing import List

from models import CurrencyRate
from interfaces.currency_rates_provider import CurrencyRatesProvider

class ProviderContainer:
    providers: List[CurrencyRate] = []

    @staticmethod
    def register(provider: CurrencyRatesProvider):
        ProviderContainer.providers.append(provider)
        return provider
