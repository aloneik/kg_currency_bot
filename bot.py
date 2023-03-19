import telebot
import os

from dotenv import load_dotenv

from bakai import BakaiRatesProvider


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
        bot.send_message(
            chat_id=chat_id,
            text=f"Курс {bakai_rub_rate.code}-KGS в Бакай банке:\n  Наличными:\n    Покупка: {bakai_rub_rate.cash_buy}\n    Продажа: {bakai_rub_rate.cash_sell}\n  Безналичными:\n    Покупка: {bakai_rub_rate.non_cash_buy}\n    Продажа: {bakai_rub_rate.non_cash_sell}"
        )
    except Exception as ex:
        # Send an error message
        print(ex)
        bot.send_message(chat_id=chat_id, text=f"Что-то пошло не так. Невозможно получить курсы валют.")

# Start the bot
bot.polling(none_stop=True)