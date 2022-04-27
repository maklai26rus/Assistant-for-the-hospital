import json
import datetime


class TextBot:
    """Класс с глобальными переменными


    :return
    """

    def __init__(self):
        self.main_unit = read_json_file('json/main_unit.json')
        self.hospital = read_json_file('json/hospital.json')
        self.polyclinic = read_json_file('json/polyclinic.json')
        self.administration = read_json_file('json/administration.json')
        self.region = read_json_file('json/region.json')
        self.step = 8
        self.step_0 = 0
        self.step_5 = self.step
        self.dept = None


class UserData:

    def __init__(self):
        self.direction = None
        self.fio_children = None
        self.fio_people = None
        self.id = None
        self.phone = None
        self.photo = False

        self.today = datetime.date.today()
        self.correct_date = None

    def get_date(self, text):
        """Определение правильности вводимых надых по дате"""
        try:
            _t = text.split('.')
            _get_start = datetime.date(int(_t[2]), int(_t[1]), int(_t[0]))
        except AttributeError:
            _get_start = datetime.date(text.year, text.month, text.day)
        _today = datetime.date(self.today.year, self.today.month, self.today.day)
        if _get_start < _today:
            return _get_start
        else:
            return None


def read_json_file(file):
    """
    Читаем json file
    :param file:
    :return: возращает словарь из json
    """
    with open(file, 'r', encoding='utf-8') as ff:
        j = json.load(ff)
    return j


def get_date():
    _date = datetime.datetime.today()
    d = _date.strftime("%Y-%m-%d-%H %M %S")
    return d
