from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from configuration.my_settings import TextBot


class MyKeyboard:

    def __init__(self):
        self.text = TextBot()
        self.left = "⬅"
        self.right = "➡"
        self.centre = self.text.main_unit['short_menu']
        self.finish_registration = self.text.main_unit['Главное меню']

    def active_menu(self, dept, step_0, step_5):
        """

        [*************]
        [*************]
        [⬅][Меню][➡]]


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

        step = self.text.step
        keyboard = InlineKeyboardMarkup()
        inline_btn_3 = InlineKeyboardButton(self.left, callback_data=self.left)
        inline_btn_menu = InlineKeyboardButton(self.centre, callback_data='/menu')
        inline_btn_4 = InlineKeyboardButton(self.right, callback_data=self.right)

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

    def main_menu(self):
        """
        Основоное меню
        :return:
        """
        keyboard = InlineKeyboardMarkup()
        keyboard.add(
            InlineKeyboardButton(text=self.text.main_unit['phones_menu'], callback_data='/phones'))
        keyboard.add(InlineKeyboardButton(text=self.text.main_unit['address_menu'], callback_data='/location'))
        keyboard.add(InlineKeyboardButton(text=self.text.main_unit['register'], callback_data='/register'))
        return keyboard

    def menu_phones(self):
        """
        Меню телефонов
        выдает список по вывобру нужной котегории
        :return:
        """
        keyboard = InlineKeyboardMarkup()

        keyboard.add(
            InlineKeyboardButton(text=self.text.main_unit['hospital'],
                                 callback_data='/hospital', ))
        keyboard.add(
            InlineKeyboardButton(text=self.text.main_unit['polyclinic'],
                                 callback_data='/polyclinic'))

        keyboard.add(
            InlineKeyboardButton(text=self.text.main_unit['administration'],
                                 callback_data='/administration'))

        keyboard.add(InlineKeyboardButton(self.text.main_unit['menu'], callback_data='/menu'))
        return keyboard

    def menu_foot(self):
        """
        Финальное меню
        Появляется после выбора пользователя
        :return:
        """
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(self.text.main_unit['menu'], callback_data='/menu'))
        return keyboard

    def telephone_keys(self):
        """Блокировка клавиатуры
        при нажатие запрашивает данные отпользователя
        """
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard.add(KeyboardButton(text=f"{self.text.main_unit['register_phones']}", request_contact=True))
        keyboard.add(KeyboardButton(text=f"{self.text.main_unit['text_not']}"))
        return keyboard

    def regions_keys(self):
        """Блокировка клавиатуры
        при нажатие запрашивает данные отпользователя
        """
        keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
        [keyboard.add(KeyboardButton(text=f"{v}")) for v in self.text.region['регион']]
        return keyboard
