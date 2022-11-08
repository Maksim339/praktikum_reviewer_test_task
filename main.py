# Можно импортировать только один модуль, а не всю библиотеку
import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Можно написать метод, который будет преобразовывать строку в дату
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        # Название переменной не раскрывает её назначения
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    # Можно сделать property метод
    def get_today_stats(self):
        today_stats = 0
        # Переменные принято называть нижним регистром
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    # Можно сделать property метод
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # Здесь нужно сократить условие и само условие вынести в отдельную переменную
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Также из метода можно сделать property
    # И нужно правильно документировать функцию, оборачиваю в тройные кавычки
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Здесь можно обойтись без else, сразу возвращать строку
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Неправильно применен символ двойное равно, а также ошибка в логике
            # так как присваивается переменной с остатком константа
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # В return не нужно использовать дополнительные скобки
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # Это условие лишнее, можно просто в конце возвращать общий return
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # Так как везде используется f-str тут тоже логичнее использовать этот метод
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Лишний метод, эта функция итак наследуется от родителя
    def get_week_stats(self):
        super().get_week_stats()
