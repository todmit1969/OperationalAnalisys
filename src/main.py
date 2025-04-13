from datetime import datetime
from pandas import to_datetime
from pathlib import Path
import pandas as pd
from src.utils import exchange_rate, greeting, price_stocks, top_transactions, transactions, write_json,read_json

from src.services import increased_cashback, cash_by_category


def main():
    """ Главная функция, отвечающая за весь проект """
    current_date = datetime.now()
    formatted_date_not_entered = to_datetime(current_date.strftime("%Y-%m-%d %H:%M:%S"))
    print(greeting(current_date))
    user_date = input("Введите к какой дате Вам нужен отчет в формате DD.MM.YYYY: ")
    if not user_date or user_date == "":
        result_cards = transactions(formatted_date_not_entered)
        result_top = top_transactions(formatted_date_not_entered)
        print(transactions(formatted_date_not_entered))
    else:
        formatted_date = to_datetime(to_datetime(user_date).strftime("%Y-%m-%d %H:%M:%S"))
        result_cards = transactions(formatted_date)
        result_top = top_transactions(formatted_date)
        print(transactions(formatted_date))

    result_exchange = exchange_rate()
    result_stock = price_stocks()

    result = {
        "greeting": greeting(current_date),
        "cards": result_cards,
        "top_transactions": result_top,
        "currency_rates": result_exchange,
        "stock_prices": result_stock
    }
    file_to_write = "operations_data.json"
    write_json(file_to_write, result)
    read_json(file_to_write)
    print(result)

    current_dir = Path(__file__).parent.parent.resolve()
    file_path_excel = current_dir / 'data' / 'operations.xlsx'
    data = pd.read_excel(file_path_excel).to_dict("records")

    cashback = increased_cashback(data, 2021, 10)
    supposed_cashback = cash_by_category(cashback)
    print(supposed_cashback)

if __name__ == "__main__":
    main()
