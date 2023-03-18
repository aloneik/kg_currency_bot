import telebot
from dotenv import load_dotenv
import requests
import os

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
        bakai_url = "https://bakai.bank/api/v1/exchangeRates"
        bakai_response = requests.get(bakai_url)
        bakai_data = bakai_response.json()
        bakai_rub_rate = bakai_data['rates']['RUB']

        # Send a message with ruble exchange rates from both banks
        bot.send_message(chat_id=chat_id, text=f"Курс рубля в КГБ: {kgb_rub_rate}\nКурс рубля в Бакай: {bakai_rub_rate}")
    except:
        # Send an error message
        bot.send_message(chat_id=chat_id, text=f"Что-то пошло не так. Невозможно получить курсы валют.")

# Start the bot
bot.polling(none_stop=True)