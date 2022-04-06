import json


def read_json_file():
    with open('phones.json', 'r', encoding='utf-8') as ff:
        j = json.load(ff)
    return j


class TextBot:
    """Класс текст бота

    :return медоды возращают текст нужной категории
    """

    def __init__(self):
        self.message = self.main_text()
        self.date_json = read_json_file()

    def main_text(self):
        """Основной текст"""
        message = {'welcome': 'Добро пожаловать',
                   'telephone_directory': 'Модуль telephone_directory в разработке',
                   'print': 'Модуль print в разработке',
                   'location': 'Модуль location в разработке',
                   'development': 'Модуль development в разработке',
                   'test': 'Модуль test в разработке',

                   }

        return message
