from pandas import to_datetime

from src.utils import greeting, transactions, top_transactions, exchange_rate, price_stocks
from datetime import datetime


def main():
    """ Главная функция, отвечающая за весь проект """
    current_date = datetime.now()
    formatted_date_not_entered = to_datetime(current_date.strftime("%Y-%m-%d %H:%M:%S"))
    print(greeting(current_date))
    user_date = input("Введите к какой дате Вам нужен отчет в формате DD.MM.YYYY: ")
    if not user_date or user_date == "":
        print(transactions(formatted_date_not_entered))
    else:
        formatted_date = to_datetime(to_datetime(user_date).strftime("%Y-%m-%d %H:%M:%S"))
        print(transactions(formatted_date))

    print(top_transactions(formatted_date))
    print(exchange_rate())
    print(price_stocks())


if __name__ == "__main__":
    main()