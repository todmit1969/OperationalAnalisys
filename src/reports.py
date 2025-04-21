from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import logging
import os

import pandas as pd


current_dir = Path(__file__).parent.parent.resolve()
file_path_expenses = current_dir/'logs'/'expenses.txt' #.encode("utf-8").decode("unicode_escape")
logging.basicConfig(
    filename=file_path_expenses,
    filemode="a+",
    format="%(levelname)s:%(name)s:Request time: %(asctime)s",
    level=logging.INFO
)

logger = logging.getLogger()
file_handler = logging.FileHandler(file_path_expenses)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

current_dir = Path(__file__).parent.parent.resolve()
file_path_excel = current_dir/'data'/'operations.xlsx'
# print(file_path_excel)


def expenses_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция, которая принимает на вход: датафрейм с транзакциями, название категории,
    опциональную дату. Если дата не передана, то берется текущая дата. Функция возвращает
    траты по заданной категории за последние три месяца (от переданной даты).
    """

    if date is None:
        date = datetime.now().date()
        logger.info("Дата не введена. Принимаем текущую дату.")

    try:
        date = pd.to_datetime(date, dayfirst=True)
    except ValueError:
        raise ValueError("Invalid date format. Please use 'DD.MM.YYYY'.")
        logger.error("Invalid date format. Please use 'DD.MM.YYYY'.")

    df = pd.read_excel(file_path_excel) if isinstance(transactions, pd.DataFrame) else transactions
    logger.info("Открывается ексель файл.")
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    filtered_transactions = df[df['Категория'] == category]
    logger.info("Транзакции отфильтрованы по Категории.")
    start_date = date - timedelta(days=90)
    end_date = date

    recent_transactions = filtered_transactions[
        (pd.to_datetime(filtered_transactions['Дата операции'], dayfirst=True) >= start_date) &
        (pd.to_datetime(filtered_transactions['Дата операции'], dayfirst=True) <= end_date)
    ]
    logger.info("Отфильтрованы последние транзакции.")
    return recent_transactions.to_dict('records')


if __name__ == '__main__':
    print(expenses_by_category(pd.read_excel(file_path_excel), 'Переводы', '23.08.2018'))
