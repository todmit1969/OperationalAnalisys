import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv


pd.options.mode.copy_on_write = True
file_path_excel = ("../data/operations.xlsx").encode("utf-8").decode("unicode_escape")


def greeting(current_date: datetime):
    """ Функция приветствующая в зависимости от времени суток"""

    hour = current_date.hour

    if 0 <= hour < 6 or 22 <= hour <= 23:
        return "Доброй ночи"
    elif 17 <= hour <= 22:
        return "Добрый вечер"
    elif 7 <= hour <= 11:
        return "Доброе утро"
    else:
        return "Добрый день"


def transactions(date_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция извлекащая детали транзакций для каждой карты
    """
    df = pd.read_excel(file_path_excel)

    # Фильтрация транзакций за указанный месяц
    df_filtered = df.loc[
         (pd.to_datetime(df['Дата операции'], dayfirst=True) <= date_time) &
         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= date_time.replace(day=1))
     ]
    df_filtered = df_filtered.to_dict(orient="records", into=dict)

    card_data = {}
    for transaction in df_filtered:
        if isinstance(transaction["Номер карты"], str) and transaction["Номер карты"].startswith("*"):
            last_digits = transaction["Номер карты"][-4:]
            if last_digits in card_data:
                continue
            card_data[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
            if transaction["Сумма операции"] < 0:
                card_data[last_digits]["total_spent"] += round(transaction["Сумма операции"] * -1, 1)
                card_data[last_digits]["cashback"] += transaction.get("Бонусы (включая кэшбэк)", 0.0)

    return list(card_data.values())

    # Расчет кэшбека
    # df_filtered.loc[:, 'кэшбек'] = df_filtered['Сумма операции с округлением'] // 100
    # sales_by_card = df_filtered.groupby('Номер карты')[['Сумма операции с округлением', 'кэшбек']].sum()
    # sorted_sales = sales_by_card.sort_values(by='Сумма операции с округлением', ascending=False)

    # return sorted_sales.to_dict(orient="records", into=dict)


def top_transactions(date_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция извлекащая 5 топ транзакций по сумме платежа.
    """
    sorted_top_5 = {'date', 'amount', 'category', 'description'}

    df = pd.read_excel(file_path_excel)

    # # Фильтрация транзакций за указанный месяц
    df_filtered = df.loc[
         (pd.to_datetime(df['Дата операции'], dayfirst=True) <= date_time) &
         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= date_time.replace(day=1))
     ]

    # df_filtered = df_filtered.do_dict(orient = "records")

    filtered_df = df_filtered.copy()

    filtered_df = filtered_df.loc[
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) <= date_time) &
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) >= date_time.replace(day=1))
        ]
    filtered_df = list(filtered_df.to_dict(orient="records"))
    filtered_df.sort(key=lambda x: x["Сумма операции"], reverse=True)
    top_5_transactions = list(filtered_df[:5])
    print(top_5_transactions)
    for item in top_5_transactions:
        sorted_top_5["date"] = item["Дата платежа"]
        sorted_top_5["amount"] = item["Сумма платежа"]
        sorted_top_5["category"] = item["Категория"]
        sorted_top_5["description"] = item["Описание"]

    print(sorted_top_5)

    return sorted_top_5


def exchange_rate(currency_list: list[str] = ["USD", "EUR"], to_currency: str = "RUB") -> list:
    """
    Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API.
    """
    load_dotenv()
    API_KEY_exchange = os.getenv("API_KEY_exchange")
    new_currency_list = []

    for currency in currency_list:
        url = (f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}"
               f"&from={currency}&amount=1")
        headers = {"apikey": API_KEY_exchange}
        response = requests.get(url, headers=headers)
        result = response.json()
        currency_value = result.get('result')

        if currency_value:
            new_currency_list.append({
                                        "currency": currency,
                                        "rate": currency_value
                                    })
        else:
            print("Ошибка: ключ 'result' не найден в ответе для:", currency)

    return new_currency_list


def price_stocks() -> list:
    """
    Функция, которая извлекает цены акций из списка S&P 500
    путем вызова внешнего API
    """
    load_dotenv()
    API_KEY_stocks = os.getenv("API_KEY_stocks")
    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stock = []

    for stock in stocks_list:
        response = requests.get(f"https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY_stocks}")

        result = response.json()
        price_element = result.get('price')
        if price_element:
            price_stock.append({
                                "stock": stock,
                                "price": price_element
                                })
        else:
            print(f"Ошибка: ключ {result} не найден в ответе для: ", stock)

    return price_stock


def read_excel(filename: str, datetime_to_timestamp: bool = True) -> pd.DataFrame:
    """Функция для чтения excel файла"""
    operations_df = pd.read_excel(filename)
    if datetime_to_timestamp:
        operations_df["Дата операции"] = pd.to_datetime(operations_df["Дата операции"], dayfirst=True)
    return operations_df


def write_json(file_path: str, data: list) -> None:
    """ Открытие и запись json данных"""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
