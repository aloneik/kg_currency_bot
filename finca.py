import requests

from typing import Union, Self, Iterable, List
from lxml import etree

from models.currency_rate import CurrencyRate
from interfaces.currency_rates_provider import CurrencyRatesProvider


class FincaRatesProvider(CurrencyRatesProvider):
    NAME = "ФИНКА"
    _finca_main_page_url = "https://fincabank.kg/"

    @staticmethod
    def _get_currency_rates() -> List[CurrencyRate]:
        finca_response = requests.get(FincaRatesProvider._finca_main_page_url)
        finca_main_page = finca_response.text

        tree = etree.HTML(finca_main_page)

        cash_rates_data = FincaRatesProvider._get_currency_rates_rows(tree)
        non_cash_rates_data = FincaRatesProvider._get_currency_rates_rows(tree, non_cash=True)

        rates = FincaRatesProvider._parse_rates_data(cash_rates_data, non_cash_rates_data)

        return rates

    @staticmethod
    def _parse_rates_data(cash_data: etree.Element, non_cash_data: etree.Element) -> List[CurrencyRate]:
        rates = []
        for row_cash, row_non_cash in zip(cash_data, non_cash_data):
            currency_code = row_cash[1].text
            if (len(currency_code) != 3):
                continue
            rate = CurrencyRate(code = currency_code)
            rate.cash_buy = row_cash[2].text
            rate.cash_sell = row_cash[3].text
            rate.non_cash_buy = row_non_cash[2].text
            rate.non_cash_sell = row_non_cash[3].text
            rates.append(rate)
        return rates

    def _get_currency_rates_rows(tree: etree.ElementTree, non_cash: bool = False) -> etree.Element:
       path = f"//div[@aria-labelledby='fusion-tab-{'Безналичный' if non_cash else 'Наличный'}']/div[@class='fif-planes-row']"
       currency_rates_xpath = etree.XPath(path)
       return currency_rates_xpath(tree)

    @staticmethod
    def _get_rates(rates_data: List[CurrencyRate], alphabetic_code: str) -> CurrencyRate:
        rates = next((rates for rates in rates_data if rates.code == alphabetic_code))
        if rates is None:
            raise ValueError(f"There is no currency `{alphabetic_code}` in the given currency rates")

        return rates

    @classmethod
    def get_rates(cls: Self, currency_code: Union[str, None] = None) -> tuple:
        rates_data = cls._get_currency_rates()
        if currency_code is None:
            return tuple(rates_data)

        return (cls._get_rates(rates_data, currency_code),)


if __name__ == "__main__":
    rates_data = FincaRatesProvider._get_currency_rates()
    rub_rates_data = FincaRatesProvider._get_rates(rates_data, "RUB")
    print(rub_rates_data)

    print(FincaRatesProvider.get_rates())
    print(FincaRatesProvider.get_rates("RUB"))
