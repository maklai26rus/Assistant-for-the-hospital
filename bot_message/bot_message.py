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
        self.main_unit = read_json_file('bot_message/main_unit.json')
        self.round_the_clock_hospital = read_json_file('bot_message/round_the_clock_hospital.json')
        self.consulting_diagnostic = read_json_file('bot_message/consulting_diagnostic_center.json')
