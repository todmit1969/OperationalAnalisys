import json
from datetime import datetime
from pathlib import Path
import logging
import pandas as pd
import os

from src.reports import current_dir

current_dir = Path(__file__).parent.parent.resolve()
file_path_increased_cashback = current_dir/'logs'/'increased_cashback.txt' .encode("utf-8").decode("unicode_escape")

logging.basicConfig(
    filename=file_path_increased_cashback,
    filemode="a+",
    format="%(levelname)s:%(name)s:Request time: %(asctime)s",
    level=logging.INFO
)

logger = logging.getLogger()
file_handler = logging.FileHandler(file_path_increased_cashback)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

def increased_cashback(transactions, year, month):
    """Функция фильтрует данные за год и месяц"""
    logger.info("Запускается функция для фильтрации данных")
    filtered_data = [transaction for transaction in transactions
                     if datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').year == year
                     and datetime.strptime(transaction['Дата операции'], '%d.%m.%Y %H:%M:%S').month == month]
    logger.info("Функция успешно завершена")
    return filtered_data


def cash_by_category(list_of_category):
    """Функция выводит данные сколько на каждой категории можно было заработать кешбэка в указанном месяце года"""
    cashback_by_category = {}
    for i in list_of_category:
        category = i["Категория"]
        cash = i["Бонусы (включая кэшбэк)"]
        if category not in cashback_by_category:
            cashback_by_category[category] = 0
            logger.info("Категория не найдена.")
        cashback_by_category[category] += cash
        logger.info("Кэшбек для категория добавлен.")
    json_cashback = json.dumps(cashback_by_category, indent=4, ensure_ascii=False)
    return json_cashback


if __name__ == "__main__":
    current_dir = Path(__file__).parent.parent.resolve()

    file_path_excel = current_dir / 'data' / 'operations.xlsx'
    data = pd.read_excel(file_path_excel).to_dict("records")

    cashback = increased_cashback(data, 2021, 10)
    supposed_cashback = cash_by_category(cashback)
    print(supposed_cashback)
