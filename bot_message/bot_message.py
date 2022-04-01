class TextBot:
    """Класс текст бота

    :return медоды возращают текст нужной категории
    """

    def __init__(self):
        self.messenge = self.main_text()

    def main_text(self):
        """Основной текст"""
        messenge = {'welcome': 'Добро пожаловать'

                    }
        return messenge


k = TextBot()
# print(TextBot.main_text)

