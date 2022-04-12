import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_message.bot_message import TextBot

from decouple import config

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)
TEXT = TextBot()
PHONES_COM = ['/polyclinic', '/hospital', '>>', '<<']


@bot.message_handler(content_types=['text'])
def run(message):
    """
    Начала работы программы. Отрабатывает комманды полученные отпользователя


    :param message:
    :return:
    """
    if message.text == '/start':
        start_menu(message)
    # elif message.text == '/hospital':
    #     phone_processing(message)
    # elif message.text == '/polyclinic':
    #     consulting_diagnostic_center(message)
    elif message.text == '/location':
        get_location(message)
    else:
        bot.send_message(message.chat.id, TEXT.main_unit['ERROR'])


def start_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(text=TEXT.main_unit['phones_menu'], callback_data='/phones'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=TEXT.main_unit['address_menu'], callback_data='/location'))
    bot.send_message(message.from_user.id,
                     f"*{TEXT.main_unit['Добро пожаловать']}*\n",
                     reply_markup=keyboard, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def message_processing(message):
    """
    Функци отлавливание сообщений от пользователя
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, TEXT.hospital['ERROR'])


@bot.callback_query_handler(func=lambda call: call.data == '/phones')
def callback_phones(call):
    """
    Отпработка нажития команды /phones
    :param call:
    :return:
    """

    keyboard = telebot.types.InlineKeyboardMarkup()
    if call.data == '/phones':
        keyboard.add(
            telebot.types.InlineKeyboardButton(text=TEXT.main_unit['hospital'],
                                               callback_data='/hospital', ))
        keyboard.add(
            telebot.types.InlineKeyboardButton(text=TEXT.main_unit['polyclinic'],
                                               callback_data='/polyclinic'))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"*{TEXT.main_unit['phones']}*", parse_mode="Markdown",
                              reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in PHONES_COM)
def callback_phones_com(call):
    """
    Отпработка нажития команд PHONES_COM
    :param call:
    :return:
    """
    keyboard = telebot.types.InlineKeyboardMarkup()

    if call.data == "/hospital":
        TEXT.dept = [v for v in TEXT.hospital['Телефонная книга']]
    elif call.data == "/polyclinic":
        TEXT.dept = [v for v in TEXT.polyclinic['Телефонная книга']]

    if call.data == '>>':
        TEXT.step_0 += TEXT.step
        TEXT.step_5 += TEXT.step
    elif call.data == '<<':
        TEXT.step_0 -= TEXT.step
        TEXT.step_5 -= TEXT.step

    if TEXT.step_0 <= -1:
        [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
         TEXT.dept[0:TEXT.step]]
        keyboard.add(InlineKeyboardButton('>>', callback_data='>>'))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"*{TEXT.main_unit['hospital']}*", parse_mode="Markdown",
                              reply_markup=keyboard)
    elif TEXT.step_5 <= len(TEXT.dept):
        [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
         TEXT.dept[TEXT.step_0:TEXT.step_5]]

        inline_btn_3 = InlineKeyboardButton('<<', callback_data='<<')
        inline_btn_4 = InlineKeyboardButton('>>', callback_data='>>')

        keyboard.row(inline_btn_3, inline_btn_4)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"*{TEXT.main_unit['hospital']}*", parse_mode="Markdown",
                              reply_markup=keyboard)
    elif TEXT.step_5 >= len(TEXT.dept):
        [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
         TEXT.dept[len(TEXT.dept) - TEXT.step:TEXT.step_5]]
        keyboard.add(InlineKeyboardButton('<<', callback_data='<<'))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"*{TEXT.main_unit['hospital']}*", parse_mode="Markdown",
                              reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == '/location')
def callback_location(call):
    """
    Локация
    :param call:
    :return:
    """
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown")
    bot.send_location(call.message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])


@bot.callback_query_handler(func=lambda call: True)
def callback_true(call):
    """
    Ловим последний калбек для отображения данных
    :param call:
    :return:
    """
    # if call.data == '/menu':
    #     start_menu(call.message)

    if call.data in TEXT.hospital['Телефонная книга']:
        _phone_dict = TEXT.hospital['Телефонная книга'][call.data]['Телефон']
    elif call.data in TEXT.polyclinic['Телефонная книга']:
        _phone_dict = TEXT.polyclinic['Телефонная книга'][call.data]['Телефон']

    t = f"{call.data.replace('/', '')}:\n"
    for p, v in _phone_dict.items():
        t += f"{p} : {v} \n"

    TEXT.step_0 = 0
    TEXT.step_5 = 5
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{t}")


# def phone_processing(message):
#     """
#     Обработка телефоного справочника hospital.json
#     :param message:
#     :return:
#     """
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
#      TEXT.hospital['Телефонная книга']]
#     bot.send_message(message.chat.id,
#                      f"Выбедите нужное отделение \n",
#                      reply_markup=keyboard)
#
#
# def consulting_diagnostic_center(message):
#     """
#     Обработка телефоного справочника consulting_diagnostic.json
#     :param message:
#     :return:
#     """
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
#      TEXT.polyclinic['Телефонная книга']]
#     bot.send_message(message.chat.id,
#                      f"Выбедите нужное отделение \n",
#                      reply_markup=keyboard)


def get_location(message):
    bot.send_message(message.chat.id, f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown")
    # bot.send_location(message.chat.id, latitude=45.03941329750142, longitude=41.93704757646342)
    bot.send_location(message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])


def main():
    # bot.infinity_polling()
    bot.polling(timeout=10)


if __name__ == "__main__":
    main()
