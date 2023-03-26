import telebot
import os

from dotenv import load_dotenv

from bakai import BakaiRatesProvider
from response_image_builder import ResponseImageBuilder

load_dotenv()  # Take environment variables from .env.

# Your bot token
TOKEN = os.getenv("BOT_TOKEN")

# Create an instance of the bot
bot = telebot.TeleBot(TOKEN)

# Function to send a message in Telegram
@bot.message_handler(commands=['rate'])
def send_message(message):
    chat_id = message.chat.id

    try:
        # Get the ruble exchange rate from Bakai bank API
        bakai_rub_rate = BakaiRatesProvider.get_rates("RUB")[0]

        bank = "Бакай"
        text = build_response_text(bakai_rub_rate, bank)
        
        response_image_builder = ResponseImageBuilder()
        response_image = response_image_builder.build_image(text)

        bot.send_photo(chat_id=chat_id, photo=response_image)
    except Exception as ex:
        # Send an error message
        print(ex)
        bot.send_message(chat_id=chat_id, text=f"Что-то пошло не так. Невозможно получить курсы валют.")

def build_response_text(rate, bank):
    return (
        f"Курс {rate.code}-KGS в банке {bank}:\n \n"
        f"Наличными:\n"
        f"    Покупка: {rate.cash_buy}\n"
        f"    Продажа: {rate.cash_sell}\n \n"
        f"Безналичными:\n"
        f"    Покупка: {rate.non_cash_buy}\n"
        f"    Продажа: {rate.non_cash_sell}"
    )

# Start the bot
bot.polling(none_stop=True)
