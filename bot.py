import telebot
import os
import logging
import datetime

from collections import namedtuple
from typing import List
from string import Template
from dotenv import load_dotenv

from utils.response_image_builder import ResponseImageBuilder
from models.currency_rate import CurrencyRate
from interfaces.currency_rates_provider import CurrencyRatesProvider
from providers.provider_container import ProviderContainer


BankRates = namedtuple("BankRates", ["name", "rates"])

# Take environment variables from .env.
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["rate"])
def send_message(message):
    chat_id = message.chat.id

    rates = get_rates_data()
    response_text = build_response_text(rates)

    image_builder = ResponseImageBuilder()
    response_image = image_builder.build_image(response_text)

    bot.send_photo(chat_id=chat_id, photo=response_image)

def get_rates_data(currency: str="RUB") -> List[BankRates]:
    rates = []
    for provider in ProviderContainer.providers:
        try:
            rates.append(BankRates(provider.NAME, get_rates(provider(), currency)))
        except Exception as ex:
            print(ex)

    return rates

def build_response_text(rates: List[BankRates]) -> str:
    response_text = ""
    row_template = Template("$title:\n    Покупка: $buy\n    Продажа: $sell\n")
    for bank_rate in rates:
        rate = bank_rate.rates
        response_text += f"Курс {rate.code}-KGS в банке {bank_rate.name}:\n"

        if rate.cash_buy is not None:
            response_text += row_template.substitute(title="Наличными", buy=rate.cash_buy, sell=rate.cash_sell)
        if rate.non_cash_buy is not None:
            response_text += row_template.substitute(title="Безналичными", buy=rate.non_cash_buy, sell=rate.non_cash_sell)

        response_text += "\n"
    return response_text

def get_rates(provider: CurrencyRatesProvider, currency_code: str) -> CurrencyRate:
    return provider.get_rates(currency_code)[0]

def init_logging():
    time = datetime.datetime.now()
    time_str = time.strftime(r"%d_%m_%Y_%H_%M_%S")
    format = "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
    logging.basicConfig(level=logging.INFO, filename=f"currency_bot_{time_str}.log", encoding="cp1251", format=format)

if __name__ == "__main__":
    init_logging()
    bot.polling(none_stop=True)
