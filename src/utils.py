import json
from datetime import datetime
import pandas as pd
import os
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
    data = pd.read_excel(file_path_excel)
    json_data = data.to_json()
    # Фильтрация транзакций за указанный месяц
    df_filtered = df.loc[
         (pd.to_datetime(df['Дата операции'], dayfirst=True) <= date_time) &
         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= date_time.replace(day=1))
     ]

    # Расчет кэшбека
    df_filtered.loc[:, 'кэшбек'] = df_filtered['Сумма операции с округлением'] // 100
    sales_by_card = df_filtered.groupby('Номер карты')[['Сумма операции с округлением', 'кэшбек']].sum()
    sorted_sales = sales_by_card.sort_values(by='Сумма операции с округлением', ascending=False)

    return sorted_sales.to_dict(orient="records", into=dict)


def top_transactions(date_time: pd.Timestamp) -> pd.DataFrame:
    """
    Функция извлекащая 5 топ транзакций по сумме платежа.
    """

    df = pd.read_excel(file_path_excel)

    # # Фильтрация транзакций за указанный месяц
    df_filtered = df.loc[
         (pd.to_datetime(df['Дата операции'], dayfirst=True) <= date_time) &
         (pd.to_datetime(df['Дата операции'], dayfirst=True) >= date_time.replace(day=1))
     ]
    #print(df_filtered)
    filtered_df = df.copy()

    filtered_df = filtered_df.loc[
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) <= date_time) &
        (pd.to_datetime(filtered_df['Дата операции'],
                        format="%d.%m.%Y %H:%M:%S", dayfirst=True) >= date_time.replace(day=1))
        ]

    top_5_transactions = (filtered_df.sort_values(by='Сумма операции с округлением', ascending=False).head(5)).to_dict(orient='records')

    return top_5_transactions


def exchange_rate(currency_list: list[str] = ["USD", "EUR"], to_currency: str = "RUB") -> list:
    """
    Функция, которая извлекает курсы обмена для USD и EUR к RUB
    путем вызова внешнего API.
    """
    load_dotenv()
    API_KEY_exchange = "MV9jtNrG3n9b0WjrqfhVFOmonvCZXWrn"
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
    путем вызова внешнего API.
    """
    load_dotenv()
    API_KEY_stocks =os.getenv("API_KEY_stocks")
    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stock = []

    for stock in stocks_list:
        response = requests.get(f"https://api.twelvedata.com/price?symbol={stock}&apikey={API_KEY_stocks}")

        result = response.json()
        price_element = result.get('price')
        if price_element:
            price_stock.append({
                                "stock":stock,
                                "price":price_element
                                })
        else:
            print(f"Ошибка: ключ {result} не найден в ответе для: ", stock)

    return price_stock