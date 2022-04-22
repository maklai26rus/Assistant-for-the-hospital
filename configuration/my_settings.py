import json
import datetime


class TextBot:
    """Класс с глобальными переменными


    :return
    """

    def __init__(self):
        self.main_unit = read_json_file('configuration/main_unit.json')
        self.hospital = read_json_file('configuration/hospital.json')
        self.polyclinic = read_json_file('configuration/polyclinic.json')
        self.administration = read_json_file('configuration/administration.json')
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
        self.birth_date = None
        self.id = None
        self.phone = None
        self.photo = False


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
