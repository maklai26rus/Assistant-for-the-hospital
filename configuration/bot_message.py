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
    """Класс с глобальными переменными


    :return
    """

    def __init__(self):
        self.main_unit = read_json_file('configuration/main_unit.json')
        self.hospital = read_json_file('configuration/hospital.json')
        self.polyclinic = read_json_file('configuration/polyclinic.json')
        self.administration = read_json_file('configuration/administration.json')
        self.step = 8
        self.step_0 = 0
        self.step_5 = self.step
        self.dept = None
