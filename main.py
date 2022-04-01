import telebot
from bot_message.bot_message import TextBot

from decouple import config

# from telegram_bot_calendar import LSTEP

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)
TEXT = TextBot()


@bot.message_handler(commands=['start', 'telephone'])
def run(message):
    print(TEXT.messenge['welcome'])
    if message.text == '/telephone':
        bot.send_message(message.chat.id, TEXT.messenge['welcome'])
    else:
        print('ne telefon')
    # command_user()


# @bot.message_handler(content_types=['text'])
# def command_user(message):
#     print(TEXT.messenge['welcome'])
#     bot.send_message(message.chat.id, TEXT.messenge['welcome'])


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
