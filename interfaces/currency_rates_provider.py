from abc import ABC, abstractmethod
from typing import Union, Self, Tuple

from models.currency_rate import CurrencyRate

class CurrencyRatesProvider(ABC):
    """Returns a tuple of CurrencyRate values"""
    @classmethod
    @abstractmethod
    def get_rates(cls: Self, currency_code: Union[str, None] = None) -> Tuple[CurrencyRate]:
        pass
