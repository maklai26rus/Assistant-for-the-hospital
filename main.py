import os
# import datetime

import telebot
from configuration.my_settings import TextBot, UserData, get_date

from decouple import config

from configuration.my_keybord import MyKeyboard

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)
TEXT = TextBot()
KEYBOARD = MyKeyboard()
PHONES_COM = ['/polyclinic', '/hospital', '/administration', KEYBOARD.right, KEYBOARD.left]
USER = UserData()


# USER.date = datetime.datetime.today()


@bot.message_handler(content_types=['text'])
def run(message):
    """
    Начала работы программы. Отрабатывает комманды полученные отпользователя


    :param message:
    :return:
    """
    if message.text == '/start':
        USER.id = message.chat.id
        bot.send_message(message.from_user.id,
                         f"*{TEXT.main_unit['Добро пожаловать']}*\n",
                         reply_markup=KEYBOARD.main_menu(), parse_mode="Markdown")
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
                          reply_markup=KEYBOARD.menu_phones())


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

    if call.data == KEYBOARD.right:
        TEXT.step_0 += TEXT.step
        TEXT.step_5 += TEXT.step
    elif call.data == KEYBOARD.left:
        TEXT.step_0 -= TEXT.step
        TEXT.step_5 -= TEXT.step

    keyboard = KEYBOARD.active_menu(dept=TEXT.dept, step_0=TEXT.step_0, step_5=TEXT.step_5)

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
    """
    Обработка команнды запись от пользователя
    :param call:
    :return:
    """
    bot.send_message(chat_id=call.message.chat.id, text=f"{TEXT.main_unit['operator']}",
                     reply_markup=KEYBOARD.telephone_keys())

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{TEXT.main_unit['processing']}", parse_mode="Markdown")

    bot.register_next_step_handler(call.message, data_processing)


def data_processing(message):
    """
    Заполнение данных на талон
    :param message:
    :return:
    """
    if message.text == TEXT.main_unit['text_not']:
        bot.send_message(message.chat.id, text=TEXT.main_unit['text_no_phones'])
        foot_menu(message)
    else:
        foot_menu(message)
        try:
            USER.phone = message.contact.phone_number
        except AttributeError:
            print(USER.phone)
        USER.fio_people = message.chat.first_name
        USER.id = message.chat.id

        bot.send_message(message.chat.id, f"*{TEXT.main_unit['text_add_direction']}*", parse_mode="Markdown")
        USER.photo = True
        bot.register_next_step_handler(message, direction_processing)


@bot.message_handler(content_types=['photo', 'text'])
def direction_processing(message):
    """
    Обработчи получения фотографии с направлением

    :param message:
    :return:
    """
    if USER.photo:
        try:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            if os.path.isdir(f'photo/{message.chat.id}'):
                src = f'photo/{message.chat.id}/{get_date()}' + '.' + \
                      file_info.file_path.split('.')[1]
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)
                bot.reply_to(message, TEXT.main_unit['text_photo'])
            else:
                os.mkdir(f'photo/{message.chat.id}')

            bot.send_message(chat_id=message.chat.id, text=f"{TEXT.main_unit['text_region']}",
                             reply_markup=KEYBOARD.regions_keys())
            USER.photo = False
            bot.register_next_step_handler(message, xxx)

        except TypeError:
            bot.send_message(message.chat.id, f"{TEXT.main_unit['text_add_direction']}", parse_mode="Markdown")
            bot.register_next_step_handler(message, direction_processing)


def xxx(message):
    USER.direction = message.text
    print(USER.direction)
    print(USER.phone)
    print(USER.fio_people)


def get_location(message):
    """
    Вызывает карту. с указаными кооринатами
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown")
    bot.send_location(message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])


def foot_menu(message):
    """
    Меню выдаваемое в конце диолога
    """
    bot.send_message(message.chat.id, TEXT.main_unit['Главное меню'], reply_markup=KEYBOARD.menu_foot())
    # bot.send_message(message.chat.id, KEYBOARD.finish_registration, reply_markup=KEYBOARD.menu_foot())


@bot.callback_query_handler(func=lambda call: call.data == '/menu')
def callback_menu(call):
    """Обработка команды /menu"""
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['Добро пожаловать']}*", parse_mode="Markdown",
                          reply_markup=KEYBOARD.main_menu())


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
