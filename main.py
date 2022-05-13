import logging
from aiogram import Bot, Dispatcher, executor, types

import os
# import datetime

# import telebot

from configuration.my_calendar import MyStyleCalendar, LSTEP
from configuration.my_settings import TextBot, UserData, get_date

from decouple import config

from configuration.my_keybord import MyKeyboard

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

# Объект бота
bot = Bot(token=SECRET_KEY_BOT)
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)

TEXT = TextBot()
KEYBOARD = MyKeyboard()
PHONES_COM = ['/polyclinic', '/hospital', '/administration', KEYBOARD.right, KEYBOARD.left]
USER = UserData()


# USER.date = datetime.datetime.today()


@dp.message_handler(commands=['start', 'location'])
async def run(message):
    """
    Начала работы программы. Отрабатывает комманды полученные отпользователя


    :param message:
    :return:
    """
    if message.text == '/start':
        USER.id = message.chat.id
        await bot.send_message(message.from_user.id,
                               f"*{TEXT.main_unit['Добро пожаловать']}*\n",
                               reply_markup=KEYBOARD.main_menu(), parse_mode="Markdown")
    elif message.text == '/location':
        await get_location(message)
        await foot_menu(message)
    else:
        await bot.send_message(message.chat.id, TEXT.main_unit['ERROR'])


@dp.callback_query_handler(text='/menu')
async def menu(call):
    USER.id = call.message.chat.id
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown",
                                reply_markup=KEYBOARD.main_menu())


@dp.callback_query_handler(text=[v for v in TEXT.polyclinic['Телефонная книга']])
async def polyclinic(call):
    _phone_dict = TEXT.polyclinic['Телефонная книга'][call.data]['Телефон']
    await phone_output(_phone_dict, call)


@dp.callback_query_handler(text=[v for v in TEXT.administration['Телефонная книга']])
async def administration(call):
    _phone_dict = TEXT.administration['Телефонная книга'][call.data]['Телефон']
    await phone_output(_phone_dict, call)


@dp.callback_query_handler(text=[v for v in TEXT.hospital['Телефонная книга']])
async def hospital(call):
    _phone_dict = TEXT.hospital['Телефонная книга'][call.data]['Телефон']
    await phone_output(_phone_dict, call)


async def phone_output(_phone_dict, call):
    try:
        t = f"{call.data.replace('/', '')}:\n"
        for p, v in _phone_dict.items():
            t += f"{p} : {v}\n"
    except UnboundLocalError as er:
        print("Ошибка словаря", er)
    TEXT.step_0 = 0
    TEXT.step_5 = TEXT.step
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{t}")
    await foot_menu(call.message)


@dp.callback_query_handler(text='/print')
async def callback_print(call):
    """
    Отпработка нажития команды /phones
    :param call:
    :return:
    """

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*Отправте файил для печати*", parse_mode="Markdown")


@dp.callback_query_handler(text='/phones')
async def callback_phones(call):
    """
    Отпработка нажития команды /phones
    :param call:
    :return:
    """

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*{TEXT.main_unit['phones']}*", parse_mode="Markdown",
                                reply_markup=KEYBOARD.menu_phones())


@dp.callback_query_handler(text=PHONES_COM)
async def callback_phones_com(call):
    """
    Отпработка нажития команд PHONES_COM
    :param call:
    :return:
    """

    _text_row = None

    if call.data == "/hospital":
        TEXT.dept = [v for v in TEXT.hospital['Телефонная книга']]
        _text_row = TEXT.main_unit['hospital']
    elif call.data == "/administration":
        TEXT.dept = [v for v in TEXT.administration['Телефонная книга']]
        _text_row = TEXT.main_unit['administration']
    elif call.data == "/polyclinic":
        TEXT.dept = [v for v in TEXT.polyclinic['Телефонная книга']]
        _text_row = TEXT.main_unit['polyclinic']

    if call.data == KEYBOARD.right:
        TEXT.step_0 += TEXT.step
        TEXT.step_5 += TEXT.step
    elif call.data == KEYBOARD.left:
        TEXT.step_0 -= TEXT.step
        TEXT.step_5 -= TEXT.step

    keyboard = KEYBOARD.active_menu(dept=TEXT.dept, step_0=TEXT.step_0, step_5=TEXT.step_5)

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*{_text_row}*", parse_mode="Markdown",
                                reply_markup=keyboard)


@dp.callback_query_handler(text='/location')
async def callback_location(call):
    """
    Показывает место положение здания
    :param call:
    :return:
    """

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown", )
    await bot.send_location(call.message.chat.id, latitude=TEXT.main_unit['latitude'],
                            longitude=TEXT.main_unit['longitude'])

    await foot_menu(call.message)


@dp.callback_query_handler(text='/register')
async def get_register(call):
    """
    Обработка команнды запись от пользователя
    :param call:
    :return:
    """
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"{TEXT.main_unit['processing']}", parse_mode="Markdown",
                                reply_markup=KEYBOARD.consent_url())

    await bot.send_message(chat_id=call.message.chat.id, text=f"{TEXT.main_unit['operator']}",
                           reply_markup=KEYBOARD.telephone_keys())


@dp.message_handler(lambda message: message.text == 'Отказ')
async def abandoning_phone(message):
    """Ловит события отказа от потверждении телефона"""

    await bot.send_message(chat_id=message.chat.id, text=f"{TEXT.main_unit['text_no_phones']}")
    await foot_menu(message)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_register(message: types.Message):
    """Стоит фильт на согласия потвердить телефон """
    USER.phone = message.contact["phone_number"]
    USER.fio_people = message.contact["first_name"]
    await bot.send_message(message.chat.id, f"Ваше Имя {USER.fio_people}? ")


async def data_processing(message):
    """
    Заполнение данных на талон
    :param message:
    :return:
    """
    if message.text == '/start':
        await run(message)
    else:

        if message.text == TEXT.main_unit['text_not']:
            await bot.send_message(message.chat.id, text=TEXT.main_unit['text_no_phones'])
            await foot_menu(message)
        else:
            await foot_menu(message)
            try:
                USER.phone = message.contact.phone_number
                USER.fio_people = message.chat.first_name
                USER.id = message.chat.id

                await bot.send_message(message.chat.id, f"*{TEXT.main_unit['text_add_direction']}*",
                                       parse_mode="Markdown")
                USER.photo = True
                # await bot.register_next_step_handler(message, direction_processing)
            except AttributeError:
                await bot.send_message(message.chat.id, text=TEXT.main_unit['text_no_phones_2'])
                await foot_menu(message)


@dp.message_handler(content_types=['photo', 'text'], )
async def direction_processing(message):
    """
    Обработчи получения фотографии с направлением

    :param message:
    :return:
    """
    if message.text == '/start':
        await run(message)
    else:
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

                await bot.send_message(chat_id=message.chat.id, text=f"{TEXT.main_unit['text_region']}",
                                       reply_markup=KEYBOARD.regions_keys())

                USER.photo = False
                await bot.register_next_step_handler(message, requesting_child_name)

            except TypeError:
                await bot.send_message(message.chat.id, f"{TEXT.main_unit['text_add_direction']}",
                                       parse_mode="Markdown")
                await bot.register_next_step_handler(message, direction_processing)


async def requesting_child_name(message):
    """
    Запрос на имя ребенка
    :param message:
    :return:
    """
    if message.text == '/start':
        await run(message)
    else:
        USER.direction = message.text
        await bot.send_message(message.chat.id, TEXT.main_unit['child_name'])
        await bot.register_next_step_handler(message, birth_date)


async def birth_date(message):
    """
    Запрос на дату рождения
    :param message:
    :return:
    """
    USER.fio_children = message.text
    await bot.send_message(message.chat.id, TEXT.main_unit['birth_date'])
    await identification_date(message.chat.id)


async def identification_date(chat_id) -> None:
    calendar, step = MyStyleCalendar(locale='ru').build()
    await bot.send_message(chat_id,
                           f"Нужно выбрать {LSTEP[step]}",
                           reply_markup=calendar)


# @dp.callback_query_handler(func=MyStyleCalendar.func())
# async def cal(c):
#     result, key, step = MyStyleCalendar(locale='ru').process(c.data)
#     if not result and key:
#         await bot.edit_message_text(f"Нужно выбрать {LSTEP[step]}",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         await bot.edit_message_text(f"Выбрана дата {result.day}.{result.month}.{result.year}",
#                               c.message.chat.id,
#                               c.message.message_id)
#         USER.correct_date = USER.get_date(result)
#         if not USER.correct_date:
#             await bot.send_message(c.message.chat.id, 'Дата не соответсвует')
#             await identification_date(c.message.chat.id)
#         else:
#             await choose_ticket(c.message)


async def choose_ticket(message):
    """
    Закантивает регистрация
    Ваше ФИО USER.fio_people
    Ребенок ФИО USER.fio_children
    Возраст ребенка USER.birth_date
    Ваш район USER.direction
    Телефон USER.phone

    :param message:
    :return:
    """
    text = f'Ваше ФИО {USER.fio_people}\nРебенок ФИО {USER.fio_children}\nВозраст ребенка {USER.correct_date}\nВаш район {USER.direction}\nТелефон {USER.phone}'
    await bot.send_message(message.chat.id, text)


async def get_location(message):
    """
    Вызывает карту. с указаными кооринатами
    :param message:
    :return:
    """
    await bot.send_message(message.chat.id, f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown")
    await bot.send_location(message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])


@dp.callback_query_handler(text='/foot')
async def foot_menu(message):
    """
    Меню выдаваемое в конце диолога
    """
    await bot.send_message(message.chat.id, TEXT.main_unit['Главное меню'], reply_markup=KEYBOARD.menu_foot())


@dp.callback_query_handler(text=lambda call: call.data == '/menu')
async def callback_menu(call):
    """Обработка команды /menu"""
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=f"*{TEXT.main_unit['Добро пожаловать']}*", parse_mode="Markdown",
                                reply_markup=KEYBOARD.main_menu())


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
