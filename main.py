import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from configuration.bot_message import TextBot

from decouple import config

from configuration.my_keybord import active_menu, main_menu, menu_phones, menu_foot

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)
TEXT = TextBot()
PHONES_COM = ['/polyclinic', '/hospital', '/administration', '>>', '<<']


@bot.message_handler(content_types=['text'])
def run(message):
    """
    Начала работы программы. Отрабатывает комманды полученные отпользователя


    :param message:
    :return:
    """
    if message.text == '/start':
        bot.send_message(message.from_user.id,
                         f"*{TEXT.main_unit['Добро пожаловать']}*\n",
                         reply_markup=main_menu(), parse_mode="Markdown")

    elif message.text == '/location':
        get_location(message)
        foot_menu(message)
    else:
        bot.send_message(message.chat.id, TEXT.main_unit['ERROR'])


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

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['phones']}*", parse_mode="Markdown",
                          reply_markup=menu_phones())


@bot.callback_query_handler(func=lambda call: call.data in PHONES_COM)
def callback_phones_com(call):
    """
    Отпработка нажития команд PHONES_COM
    :param call:
    :return:
    """
    if call.data == "/hospital":
        TEXT.dept = [v for v in TEXT.hospital['Телефонная книга']]
    elif call.data == "/administration":
        TEXT.dept = [v for v in TEXT.administration['Телефонная книга']]
    elif call.data == "/polyclinic":
        TEXT.dept = [v for v in TEXT.polyclinic['Телефонная книга']]

    if call.data == '>>':
        TEXT.step_0 += TEXT.step
        TEXT.step_5 += TEXT.step
    elif call.data == '<<':
        TEXT.step_0 -= TEXT.step
        TEXT.step_5 -= TEXT.step

    keyboard = active_menu(dept=TEXT.dept, step_0=TEXT.step_0, step_5=TEXT.step_5)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['hospital']}*", parse_mode="Markdown",
                          reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == '/location')
def callback_location(call):
    """
    Показывает место положение здания
    :param call:
    :return:
    """

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown", )
    bot.send_location(call.message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])

    foot_menu(call.message)


@bot.callback_query_handler(func=lambda call: call.data == '/register')
def get_register(call):
    TEXT.dept = [v for v in TEXT.polyclinic['Телефонная книга']]

    if call.data == '>>':
        TEXT.step_0 += TEXT.step
        TEXT.step_5 += TEXT.step
    elif call.data == '<<':
        TEXT.step_0 -= TEXT.step
        TEXT.step_5 -= TEXT.step

    keyboard = active_menu(dept=TEXT.dept, step_0=TEXT.step_0, step_5=TEXT.step_5)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['hospital']}*", parse_mode="Markdown",
                          reply_markup=keyboard)

    bot.send_message(call.message.chat.id, 'Блок в разработке')


def get_location(message):
    bot.send_message(message.chat.id, f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown")
    bot.send_location(message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])


def foot_menu(message):
    """
    Меню выдаваемое в конце диолога
    """
    bot.send_message(message.chat.id, TEXT.main_unit['Главное меню'], reply_markup=menu_foot())


@bot.callback_query_handler(func=lambda call: call.data == '/menu')
def callback_menu(call):
    """Обработка команды /menu"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['Добро пожаловать']}*", parse_mode="Markdown",
                          reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: True)
def callback_true(call):
    """
    Ловим последний калбек для отображения данных
    :param call:
    :return:
    """

    if call.data in TEXT.hospital['Телефонная книга']:
        _phone_dict = TEXT.hospital['Телефонная книга'][call.data]['Телефон']
    elif call.data in TEXT.polyclinic['Телефонная книга']:
        _phone_dict = TEXT.polyclinic['Телефонная книга'][call.data]['Телефон']
    elif call.data in TEXT.administration['Телефонная книга']:
        _phone_dict = TEXT.administration['Телефонная книга'][call.data]['Телефон']

    try:
        t = f"{call.data.replace('/', '')}:\n"
        for p, v in _phone_dict.items():
            t += f"{p} : {v} \n"
    except UnboundLocalError as er:
        print("Ошибка словаря", er)

    TEXT.step_0 = 0
    TEXT.step_5 = TEXT.step

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{t}")
    foot_menu(call.message)


def main():
    bot.infinity_polling()
    # bot.polling(timeout=1)


if __name__ == "__main__":
    main()
