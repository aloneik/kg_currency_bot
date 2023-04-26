import requests
import logging

from typing import Union, Self, Iterable

from models.currency_rate import CurrencyRate
from interfaces.currency_rates_provider import CurrencyRatesProvider
from providers.provider_container import ProviderContainer


@ProviderContainer.register
class BakaiRatesProvider(CurrencyRatesProvider):
    NAME = "Бакай"
    _bakai_currency_rates_url = "https://bakai24.bakai.kg/v1/currency_rates"
    _currencies_field = "currencies"

    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger()

    def _get_currency_rates(self) -> list:
        bakai_response = requests.get(BakaiRatesProvider._bakai_currency_rates_url)
        bakai_data = bakai_response.json()
        self._logger.info(f"Recieved data from Bakai API: {bakai_data}")

        currencies_field = BakaiRatesProvider._currencies_field
        if currencies_field not in bakai_data:
            self._logger.info("Recieved data is incorrect")
            raise ValueError(f"Response from Bakai's currency API is incorrect")

        return bakai_data[currencies_field]

    def _get_curr_codes(self, rates_data: dict) -> Iterable[str]:
        return (cr["code"] for cr in rates_data)

    def _get_rates(self, rates_data: list, alphabetic_code: str) -> dict:
        desired_rates = next(cr for cr in rates_data if cr["code"] == alphabetic_code)
        if desired_rates is None:
            self._logger.info(f"Currency code '{alphabetic_code}' not found")
            raise ValueError(f"There is no currency `{alphabetic_code}` in the given currency rates")
        
        self._logger.info(f"Found rates for '{alphabetic_code}': {desired_rates}")
        return desired_rates

    def _get_actual_rates(self, rates: dict) -> CurrencyRate:
        rate = CurrencyRate(code=rates["code"])

        cash_sell_key = "cash_sell"
        if cash_sell_key in rates:
            rate.cash_sell = rates[cash_sell_key]

        cash_buy_key = "cash_buy"
        if cash_buy_key in rates:
            rate.cash_buy = rates[cash_buy_key]

        non_cash_sell_key = "sell"
        if non_cash_sell_key in rates:
            rate.non_cash_sell = rates[non_cash_sell_key]

        non_cash_buy_key = "buy"
        if non_cash_buy_key in rates:
            rate.non_cash_buy = rates[non_cash_buy_key]

        transfer_sell_key = "trans_sell"
        if transfer_sell_key in rates:
            rate.transfer_sell = rates[transfer_sell_key]
        
        transfer_buy_key = "trans_buy"
        if transfer_buy_key in rates:
            rate.transfer_buy = rates[transfer_buy_key]

        self._logger.info(f"Conversion to CurrencyRate: {rate}")
        return rate

    def get_rates(self, currency_code: Union[str, None] = None) -> tuple:
        rates_data = self._get_currency_rates()
        codes = self._get_curr_codes(rates_data) if currency_code is None else (currency_code,)
        rates = (self._get_actual_rates(self._get_rates(rates_data, code)) for code in codes)
        return tuple(rates)


if __name__ == "__main__":
    rates_data = BakaiRatesProvider._get_currency_rates()
    rub_rates_data = BakaiRatesProvider._get_rates(rates_data, "RUB")
    rub_rate = BakaiRatesProvider._get_actual_rates(rub_rates_data)
    print(rub_rate)

    print(BakaiRatesProvider.get_rates())
    print(BakaiRatesProvider.get_rates("RUB"))
