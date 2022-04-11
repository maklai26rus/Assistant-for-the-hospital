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

        start_main(message)
    elif message.text == '/hospital':
        phone_processing(message)
    elif message.text == '/polyclinic':
        consulting_diagnostic_center(message)
    elif message.text == '/location':
        get_location(message)
    else:
        bot.send_message(message.chat.id, TEXT.main_unit['ERROR'])


def start_main(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(text='Телефоны', callback_data='/phones'))
    keyboard.add(telebot.types.InlineKeyboardButton(text=TEXT.main_unit['location'], callback_data='/location'))
    bot.send_message(message.from_user.id,
                     f"*{TEXT.main_unit['Добро пожаловать']}*\n",
                     reply_markup=keyboard, parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def message_processing(message):
    bot.send_message(message.chat.id, TEXT.hospital['ERROR'])


@bot.callback_query_handler(func=lambda call: call.data == '/phones')
def callback(call):
    """
    Отпработка нажития команды
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
        # keyboard.add(telebot.types.InlineKeyboardButton(text=TEXT.main_unit['location'], callback_data='/location'))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"*{TEXT.main_unit['phones']}*", parse_mode="Markdown",
                              reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in PHONES_COM)
def callback2(call):
    keyboard = telebot.types.InlineKeyboardMarkup()
    # dept = []
    if call.data == "/hospital":
        TEXT.dept = [v for v in TEXT.hospital['Телефонная книга']]
    elif call.data == "/polyclinic":
        TEXT.dept = [v for v in TEXT.polyclinic['Телефонная книга']]

    if call.data == '>>':
        TEXT.step_0 += 5
        TEXT.step_5 += 5
    elif call.data == '<<':
        TEXT.step_0 -= 5
        TEXT.step_5 -= 5

    if TEXT.step_0 <= -1:
        # [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
        #  TEXT.dept[0:len(TEXT.dept)]]
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

        keyboard.add(InlineKeyboardButton('<<', callback_data='<<'))

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"*{TEXT.main_unit['hospital']}*", parse_mode="Markdown",
                              reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == '/location')
def callback5(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown")
    bot.send_location(call.message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])


@bot.callback_query_handler(func=lambda call: True)
def callback6(call):
    if call.data in TEXT.hospital['Телефонная книга']:
        _phone_dict = TEXT.hospital['Телефонная книга'][call.data]['Телефон']
    elif call.data in TEXT.polyclinic['Телефонная книга']:
        _phone_dict = TEXT.polyclinic['Телефонная книга'][call.data]['Телефон']

    t = f"{call.data.replace('/', '')}:\n"
    for p, v in _phone_dict.items():
        t += f"{p} : {v} \n"

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{t}")


def method_name():
    inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
    # inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
    inline_kb_full = InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
    inline_kb_full.add(InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
    inline_btn_3 = InlineKeyboardButton('кнопка 3', callback_data='btn3')
    inline_btn_4 = InlineKeyboardButton('кнопка 4', callback_data='btn4')
    inline_btn_5 = InlineKeyboardButton('кнопка 5', callback_data='btn5')
    inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
    inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
    # inline_kb_full.insert(InlineKeyboardButton("query=''", switch_inline_query=''))
    # inline_kb_full.insert(InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
    # inline_kb_full.insert(InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
    inline_kb_full.add(
        InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))


def phone_processing(message):
    """
    Обработка телефоного справочника hospital.json
    :param message:
    :return:
    """
    keyboard = telebot.types.InlineKeyboardMarkup()
    [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
     TEXT.hospital['Телефонная книга']]
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
     TEXT.polyclinic['Телефонная книга']]
    bot.send_message(message.chat.id,
                     f"Выбедите нужное отделение \n",
                     reply_markup=keyboard)


def get_location(message):
    bot.send_message(message.chat.id, f"*{TEXT.main_unit['LOCATION']}*", parse_mode="Markdown")
    # bot.send_location(message.chat.id, latitude=45.03941329750142, longitude=41.93704757646342)
    bot.send_location(message.chat.id, latitude=TEXT.main_unit['latitude'], longitude=TEXT.main_unit['longitude'])


def main():
    # bot.infinity_polling()
    bot.polling(timeout=10)


if __name__ == "__main__":
    main()
