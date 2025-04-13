from datetime import datetime
from pathlib import Path
import pandas as pd


def increased_cashback(transactions, year, month):
    """Функция фильтрует данные за год и месяц"""
    filtered_data = [transaction for transaction in transactions
                     if datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').year == year
                     and datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').month == month]
    return filtered_data


def cash_by_category(list_of_category):
    """Функция выводит данные сколько на каждой категории можно было заработать кешбэка в указанном месяце года"""
    cashback_by_category = {}
    for i in list_of_category:
        category = i["Категория"]
        cash = i["Бонусы (включая кэшбэк)"]
        if category not in cashback_by_category:
            cashback_by_category[category] = 0
        cashback_by_category[category] += cash
    return cashback_by_category


if __name__ == "__main__":
    current_dir = Path(__file__).parent.parent.resolve()

    file_path_excel = current_dir / 'data' / 'operations.xlsx'
    data = pd.read_excel(file_path_excel).to_dict("records")

    cashback = increased_cashback(data, 2021, 10)
    supposed_cashback = cash_by_category(cashback)
    print(supposed_cashback)
