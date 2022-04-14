from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from configuration.bot_message import TextBot

TEXT = TextBot()


def active_menu(dept, step_0, step_5):
    """

    [*************]
    [*************]
    [<<][Меню][>>]]


    step = TEXT.step

    Данные которые должны прийти

    if call.data == '>>':
        TEXT.step_0 += TEXT.step
        TEXT.step_5 += TEXT.step
    elif call.data == '<<':
        TEXT.step_0 -= TEXT.step
        TEXT.step_5 -= TEXT.step

    dept = TEXT.dept = [v for v in TEXT.***['Телефонная книга']]

    :param dept: Словарь с данными которые нужно будет отобразить спиком в колонне
    :param step: Сколько элементов надо вывести на экран
    :param step_0:
    :param step_5:
    :return:
    """

    step = TEXT.step
    keyboard = InlineKeyboardMarkup()
    inline_btn_3 = InlineKeyboardButton('<<', callback_data='<<')
    inline_btn_menu = InlineKeyboardButton(TEXT.main_unit['short'], callback_data='/menu')
    inline_btn_4 = InlineKeyboardButton('>>', callback_data='>>')

    if step_0 <= -1:
        [keyboard.add(InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
         dept[0:step]]

        keyboard.row(inline_btn_menu, inline_btn_4)
        return keyboard

    elif step_5 <= len(dept):
        [keyboard.add(InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
         dept[step_0:step_5]]

        keyboard.row(inline_btn_3, inline_btn_menu, inline_btn_4)
        return keyboard

    elif step_5 >= len(dept):
        [keyboard.add(InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
         dept[len(dept) - step:step_5]]

        keyboard.row(inline_btn_3, inline_btn_menu)
        return keyboard


def main_menu():
    """
    Основоное меню
    :return:
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text=TEXT.main_unit['phones_menu'], callback_data='/phones'))
    keyboard.add(InlineKeyboardButton(text=TEXT.main_unit['address_menu'], callback_data='/location'))
    keyboard.add(InlineKeyboardButton(text=TEXT.main_unit['register'], callback_data='/register'))
    return keyboard


def menu_phones():
    """
    Меню телефонов
    выдает список по вывобру нужной котегории
    :return:
    """
    keyboard = InlineKeyboardMarkup()

    keyboard.add(
        InlineKeyboardButton(text=TEXT.main_unit['hospital'],
                             callback_data='/hospital', ))
    keyboard.add(
        InlineKeyboardButton(text=TEXT.main_unit['polyclinic'],
                             callback_data='/polyclinic'))

    keyboard.add(
        InlineKeyboardButton(text=TEXT.main_unit['administration'],
                             callback_data='/administration'))

    keyboard.add(InlineKeyboardButton(TEXT.main_unit['menu'], callback_data='/menu'))
    return keyboard


def menu_foot():
    """
    Финальное меню
    Появляется после выбора пользователя
    :return:
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(TEXT.main_unit['menu'], callback_data='/menu'))
    return keyboard
