import telebot
from bot_message.bot_message import TextBot

from decouple import config

# from telegram_bot_calendar import LSTEP

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)


@bot.message_handler(commands=['start'])
def run(message):
    command_user()


@bot.message_handler(content_types=['text'])
def command_user(message):
    print('первые шаги')


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
