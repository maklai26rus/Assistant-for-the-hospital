from telegram_bot_calendar import DetailedTelegramCalendar

LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}


class MyStyleCalendar(DetailedTelegramCalendar):
    prev_button = "⬅️"
    next_button = "➡️"
