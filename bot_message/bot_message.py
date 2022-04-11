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
        self.hospital = read_json_file('bot_message/hospital.json')
        self.polyclinic = read_json_file('bot_message/polyclinic.json')
        self.step_0 = 0
        self.step_5 = 5
        self.dept = None
