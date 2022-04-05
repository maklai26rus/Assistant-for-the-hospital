import telebot
from bot_message.bot_message import TextBot
import json

from decouple import config

# from telegram_bot_calendar import LSTEP

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)
TEXT = TextBot()


@bot.message_handler(commands=['start', 'telephone_directory', 'print', 'location'])
def run(message):
    with open('phones.json', 'r', encoding='utf-8') as ff:
        welcome = json.load(ff)
    if message.text == '/start':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton(text='Телефонный справочник', callback_data='/telephone_directory'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Печать справок', callback_data='/print'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Как проехать', callback_data='/location'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='ТЕСТ', callback_data='/test'))
        bot.send_message(message.from_user.id,
                         f"{welcome['Справочник']['Добро пожаловать']}\n",
                         reply_markup=keyboard)
        bot.register_next_step_handler(message, message_processing)

    # command_user()


@bot.message_handler(content_types=['text'])
def message_processing(message):
    if message.text == '/telephone_directory':

        bot.send_message(message.chat.id, TEXT.message['telephone_directory'])
    elif message.text == '/print':
        bot.send_message(message.chat.id, TEXT.message['print'])
    elif message.text == '/location':
        bot.send_message(message.chat.id, TEXT.message['location'])
    elif message.text == '/test':
        bot.send_message(message.chat.id, TEXT.message['test']),
        bot.register_next_step_handler(message, test_m)
    # else:
    #     bot.send_message(message.chat.id, TEXT.messenge['development'])


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == '/telephone_directory':
        test_m(call.message)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👌')
    elif call.data == '/print':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=TEXT.message['print'])
    elif call.data == '/location':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=TEXT.message['location'])
    elif call.data == '/test':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=TEXT.message['test'])
        test_m(call.message)
    else:
        t = {"/informatic": {"Информатика тех.кабинет": "+79187420881", "2": "356310"}, "/ekonomist": {"1": "357112"}}
        for p in t[call.data].items():
            print(p, )

            bot.send_message(call.message.chat.id, f"{' '.join(p)}")


def test_m(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    # k = ['Инофрматика', 'Инофрматика2', 'Инофрматика3']
    t = {"/informatic": "Инофрматика", "/ekonomist": "Экономисты"}
    for k, v in t.items():
        keyboard.add(
            telebot.types.InlineKeyboardButton(text=str(v), callback_data=k))
    bot.send_message(message.chat.id,
                     f"Выбедите нужное отделение \n",
                     reply_markup=keyboard)

    # bot.send_message(message.chat.id, 'все правильно')

    # else:
    #     bot.edit_message_text(chat_id=call.message.chat.id,
    #                           message_id=call.message.message_id, text=TEXT.messenge['development'])

    # if call.data == 'any_info':
    #     bot.edit_message_text(chat_id=call.message.chat.id,
    #                           message_id=call.message.message_id,
    #                           text='👌')
    #     bot.send_message(call.from_user.id, 'Hello')
    # elif call.data == 'any_info2':
    #     bot.send_message(call.from_user.id, 'How are you')


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
