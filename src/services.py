import json
import logging
from collections import defaultdict
from datetime import datetime
from functools import reduce
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)
current_dir = Path(__file__).parent.parent.resolve()
file_path_excel = current_dir/'data'/'operations.xlsx'


def get_cashback_categories(data, year, month):
    """
    Функция «Выгодные категории повышенного кешбэка»
    Фильтрует транзакции по указанному году и месяцу
    """
    logger.info("Анализ категорий кешбэка за %d-%02d", year, month)
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Требуется pandas DataFrame")

    data['date'] = pd.to_datetime(data['Дата операции'], dayfirst=True)

    # Фильтруем транзакции по году и месяцу
    filtered = data[(data['date'].dt.year == year) & (data['date'].dt.month == month)].copy()
    print(filtered)
    if not filtered.empty:
        cashback = (filtered.groupby('Категория')['Сумма операции с округлением']
                    .sum()
                    .div(100)
                    .round()
                    .astype(int)
                    .to_dict())
    else:
        cashback = {}


    def accumulate(acc, transaction):
        """Функция собирающая суммы по категориям"""
        category = transaction["category"]
        amount = abs(transaction["amount"])
        acc[category] += amount
        return acc

    category_cashback = reduce(accumulate, filtered, defaultdict(int))

    cashbacks = {category: round(amount * 0.01) for category, amount in category_cashback.items()}

    return json.dumps(cashbacks, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    data = pd.read_excel(file_path_excel)
   # print(data)
    print(get_cashback_categories(data, '2021', '01'))