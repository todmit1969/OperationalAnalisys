import datetime
from pathlib import Path
from typing import Union

import pandas as pd

from src.utils import greeting, exchange_rate, top_transactions, price_stocks, transactions

current_dir = Path(__file__).parent.parent.resolve()

file_path_excel = current_dir/'data'/'operations.xlsx'
print(file_path_excel)


def main_page(date_time: datetime) -> Union[list, dict]:
    """ Главная функция, принимающую на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ: """
    print(f"Входные данные: {date_time}")
    result_time = greeting(date_time)
    result_transactions = transactions(date_time)
    result_top = top_transactions(date_time)
    result_exchange = exchange_rate()
    result_price = price_stocks()

    return [result_time, result_transactions, result_top, result_exchange, result_price]


if __name__ == '__main__':

    print(f'{greeting(current_date=datetime.datetime.now())}')
   # print(main_page("2021-02-02 00:00:00"))
    # print(transactions(pd.to_datetime('29-09-2018 00:00:00', dayfirst=True)))
    date_time1 = pd.Timestamp("29-09-2018 00:00:00")
    result = transactions(date_time1)
    print("Результат транзакций:")
    print(result)
    print("Пять максимальных транзакций:")
    result = top_transactions(date_time1)
    print(result)
    print("Курсы валют:")
    print(exchange_rate())
    print("Цена акций: ")
    print(price_stocks())