import mock
import pandas as pd
import pytest
from unittest.mock import patch
from src.utils import transactions, top_transactions
import datetime


data = {
    "Дата операции": ["29.09.2018", "30.09.2018", "01.10.2018"],
    "Номер карты": ["*7197", "*4556", "*7197"],
    "Сумма операции с округлением": [186388.77, 181404.21, 150000.00],
    "Сумма операции": [186388.77, 181404.21, 150000.00],
}

df = pd.DataFrame(data)

...

@mock.patch("pandas.read_excel", return_value=df)
def test_transactions(data_time):
    result = transactions(pd.to_datetime("30-09-2018", dayfirst=True))
    expected = [
        {
            "cashback": 0.0,
            "last_digits": "7197",
            "total_spent": 0.0,
        },
        {
            "cashback": 0.0,
            "last_digits": "4556",
            "total_spent": 0.0,
        },
    ]


    assert result == expected

...

# Создаем тестовые данные
transactions_data = {
    "Категория": [
        "Продукты",
        "Переводы",
        "Продукты",
        "Продукты",
        "Переводы",
        "Продукты",
    ],
    "Дата операции": [
        "01.10.2023 17:01:37",
        "05.10.2023 17:01:37",
        "10.10.2023 17:01:37",
        "15.10.2023 17:01:37",
        "20.10.2023 17:01:37",
        "25.10.2023 17:01:37",
    ],
    "Сумма операции с округлением": [100, 200, 300, 400, 500, 600],
    "Описание": [
        "Описание",
        "Описание",
        "Описание",
        "Описание",
        "Описание",
        "Описание",
    ]
}


df_test = pd.DataFrame(transactions_data)

def test_top_transactions(monkeypatch):
    monkeypatch.setattr(pd, "read_excel", lambda _: df_test)


    # Дата для фильтрации
    test_date = datetime.datetime(2023, 10, 21, 00, 00, 00)


    # Вызов тестируемой функции
    result = top_transactions(test_date)


    assert result == [
       {
           'amount': 500,
           'category': 'Переводы',
           'date': '20.10.2023 17:01:37',
           'description': 'Описание',
       },
       {
           'amount': 400,
           'category': 'Продукты',
           'date': '15.10.2023 17:01:37',
           'description': 'Описание',
       },
       {
           'amount': 300,
           'category': 'Продукты',
           'date': '10.10.2023 17:01:37',
           'description': 'Описание',
       },
       {
           'amount': 200,
           'category': 'Переводы',
           'date': '05.10.2023 17:01:37',
           'description': 'Описание',
       },
       {
           'amount': 100,
           'category': 'Продукты',
           'date': '01.10.2023 17:01:37',
           'description': 'Описание',
       },
   ]
