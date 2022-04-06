import telebot
from bot_message.bot_message import TextBot

from decouple import config

SECRET_KEY_BOT = config('SECRET_KEY_BOT')

bot = telebot.TeleBot(SECRET_KEY_BOT)
TEXT = TextBot()


@bot.message_handler(commands=['start', 'telephone_directory', 'print', 'location'])
def run(message):
    run_bot(message)


def run_bot(message):
    if message.text == '/start':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.add(
            telebot.types.InlineKeyboardButton(text='Телефонный справочник', callback_data='/telephone_directory'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Печать справок', callback_data='/print'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='Как проехать', callback_data='/location'))
        keyboard.add(telebot.types.InlineKeyboardButton(text='ТЕСТ', callback_data='/тест'))
        bot.send_message(message.from_user.id,
                         f"*{TEXT.date_json['Справочник']['Добро пожаловать']}*\n",
                         reply_markup=keyboard, parse_mode="Markdown")
    bot.register_next_step_handler(message, message_processing)


@bot.message_handler(content_types=['text'])
def message_processing(message):
    run_bot(message)
    if message.text == '/telephone_directory':
        phone_processing(message)
        # bot.send_message(message.chat.id, TEXT.message['telephone_directory'])
    elif message.text == '/print':
        bot.send_message(message.chat.id, TEXT.message['print'])
    elif message.text == '/location':
        bot.send_message(message.chat.id, TEXT.message['location'])
    elif message.text == '/test':
        bot.send_message(message.chat.id, TEXT.message['test']),
        bot.register_next_step_handler(message, phone_processing)
    # else:
    #     bot.send_message(message.chat.id, TEXT.messenge['development'])


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == '/telephone_directory':
        phone_processing(call.message)
        # bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='👌')
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
        k = TEXT.date_json['Телефонная книга'][call.data]['Телефон']
        bot.send_message(call.message.chat.id, f"*{str(call.data.replace('/', ''))}*:", parse_mode="Markdown")
        for p, v in k.items():
            bot.send_message(call.message.chat.id, f"{p} - {v}")


def phone_processing(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    [keyboard.add(telebot.types.InlineKeyboardButton(text=str(v).replace('/', ''), callback_data=v)) for v in
     TEXT.date_json['Телефонная книга']]
    bot.send_message(message.chat.id,
                     f"Выбедите нужное отделение \n",
                     reply_markup=keyboard)


def main():
    bot.infinity_polling()


if __name__ == "__main__":
    main()
