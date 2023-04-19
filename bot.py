import telebot
import os

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

    rates = get_rates_providers()
    response_text = build_response_text(rates)

    image_builder = ResponseImageBuilder()
    response_image = image_builder.build_image(response_text)

    bot.send_photo(chat_id=chat_id, photo=response_image)

def get_rates_providers(currency: str="RUB") -> List[BankRates]:
    rates = []
    for provider in ProviderContainer.providers:
        try:
            rates.append(BankRates(provider.NAME, get_rates(provider, currency)))
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

# Start the bot
bot.polling(none_stop=True)
