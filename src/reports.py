from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import pandas as pd

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

    try:
        date = pd.to_datetime(date, dayfirst=True)
    except ValueError:
        raise ValueError("Invalid date format. Please use 'DD.MM.YYYY'.")

    df = pd.read_excel(file_path_excel) if isinstance(transactions, pd.DataFrame) else transactions

    df['Дата операции'] = pd.to_datetime(df['Дата операции'], dayfirst=True)

    filtered_transactions = df[df['Категория'] == category]

    start_date = date - timedelta(days=90)
    end_date = date

    recent_transactions = filtered_transactions[
        (pd.to_datetime(filtered_transactions['Дата операции'], dayfirst=True) >= start_date) &
        (pd.to_datetime(filtered_transactions['Дата операции'], dayfirst=True) <= end_date)
    ]
    return recent_transactions.to_dict('records')


if __name__ == '__main__':
    print(expenses_by_category(pd.read_excel(file_path_excel), 'Переводы', '23.08.2018'))
