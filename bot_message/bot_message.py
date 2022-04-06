import json


def read_json_file(file):
    """
    Читаем json file
    :param file:
    :return: возращает словарь из json
    """
    with open(file, 'r', encoding='utf-8') as ff:
        j = json.load(ff)
    return j


class TextBot:
    """Класс текст бота

    :return медоды возращают текст нужной категории
    """

    def __init__(self):
        self.message = self.main_text()
        self.main_unit = read_json_file('main_unit.json')
        self.round_the_clock_hospital = read_json_file('round_the_clock_hospital.json')
        self.consulting_diagnostic = read_json_file('consulting_diagnostic_center.json')

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
