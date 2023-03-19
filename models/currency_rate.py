from dataclasses import dataclass

@dataclass
class CurrencyRate:
    code: str = None
    non_cash_buy: float = None
    non_cash_sell: float = None
    cash_buy: float = None
    cash_sell: float = None
    transfer_buy: float = None
    transfer_sell: float = None
