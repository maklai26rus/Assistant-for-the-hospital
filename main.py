import telebot
from bot_message.bot_message import TextBot

from decouple import config

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)
TEXT = TextBot()


@bot.message_handler(content_types=['text'])
def run(message):
    """
    Начала работы программы. Отрабатывает комманды полученные отпользователя


    :param message:
    :return:
    """
    if message.text == '/start':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton(text='Круглосуточный стационар ☎️',
                                               callback_data='/round_the_clock_hospital'))
        keyboard.add(
            telebot.types.InlineKeyboardButton(text='Консультативно-диагностичский центр ☎️',
                                               callback_data='/consulting_diagnostic_center'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Печать справок', callback_data='/print'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Как проехать', callback_data='/location'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='ТЕСТ', callback_data='/тест'))
        bot.send_message(message.from_user.id,
                         f"*{TEXT.main_unit['Справочник']['Добро пожаловать']}*\n",
                         reply_markup=keyboard, parse_mode="Markdown")
    elif message.text == '/round_the_clock_hospital':
        phone_processing(message)
    elif message.text == '/print':
        bot.send_message(message.chat.id, TEXT.message['print'])
    elif message.text == '/location':
        bot.send_message(message.chat.id, TEXT.message['location'])
    elif message.text == '/test':
        bot.send_message(message.chat.id, TEXT.message['test']),
        bot.register_next_step_handler(message, phone_processing)
    else:
        bot.send_message(message.chat.id, TEXT.main_unit['ERROR'])


@bot.message_handler(content_types=['text'])
def message_processing(message):
    bot.send_message(message.chat.id, TEXT.round_the_clock_hospital['ERROR'])


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    """
    Отпработка нажития команды
    :param call:
    :return:
    """
    if call.data == '/round_the_clock_hospital':
        phone_processing(call.message)
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👌')
    elif call.data == '/consulting_diagnostic_center':
        consulting_diagnostic_center(call.message)
    elif call.data == '/print':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=TEXT.message['print'])
    elif call.data == '/location':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=TEXT.message['location'])
    elif call.data == '/тест':
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id, text=TEXT.message['test'])
        phone_processing(call.message)
    else:

        if call.data in TEXT.round_the_clock_hospital['Телефонная книга']:
            _phone_dict = TEXT.round_the_clock_hospital['Телефонная книга'][call.data]['Телефон']
        elif call.data in TEXT.consulting_diagnostic['Телефонная книга']:
            _phone_dict = TEXT.consulting_diagnostic['Телефонная книга'][call.data]['Телефон']
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"*{str(call.data.replace('/', ''))}*:", parse_mode="Markdown")

        for p, v in _phone_dict.items():
            bot.send_message(call.message.chat.id, f"{p} - {v}")


def phone_processing(message):
    """
    Обработка телефоного справочника round_the_clock_hospital.json
    :param message:
    :return:
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
     TEXT.round_the_clock_hospital['Телефонная книга']]
    bot.send_message(message.chat.id,
                     f"Выбедите нужное отделение \n",
                     reply_markup=keyboard)


def consulting_diagnostic_center(message):
    """
    Обработка телефоного справочника consulting_diagnostic.json
    :param message:
    :return:
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
     TEXT.consulting_diagnostic['Телефонная книга']]
    bot.send_message(message.chat.id,
                     f"Выбедите нужное отделение \n",
                     reply_markup=keyboard)


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
