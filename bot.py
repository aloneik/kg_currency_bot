import telebot
import os

from dotenv import load_dotenv

from bakai import BakaiRatesProvider

from PIL import Image, ImageDraw, ImageFont

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
        
        bot.send_photo(chat_id=chat_id, photo=build_response_image(text))
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
        
def build_response_image(text):
    photo = Image.new("I", (600, 670), "white")
    font = ImageFont.truetype("arial.ttf", 25)
    drawer = ImageDraw.Draw(photo)
    drawer.text((10, 10), text, font=font, fill='black')
    return photo 

# Start the bot
bot.polling(none_stop=True)