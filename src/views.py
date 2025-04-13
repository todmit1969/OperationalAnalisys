import os
from datetime import datetime
from typing import List, Any

import requests
from dotenv import load_dotenv

from config import FILE_PATH_EXCEL
from src.utils import read_excel, write_json, read_json, greeting, exchange_rate, price_stocks


def sum_expenses_transactions(transactions: List[dict]) -> float:
    """Функция возвращает сумму расходов по списку"""
    transactions =list(transactions.to_dict(orient="records"))
    expenses = 0
    for transaction in transactions:
        if transaction["Сумма операции"] < 0:
            expenses += transaction["Сумма операции"]
    return round(expenses * -1, 2)


def cards(transactions: List[dict]) -> List[dict]:
    """Функция обрабатывает данные о картах из списка"""
    transactions = list(transactions.to_dict(orient="records"))
    cards_data = {}
    for transaction in transactions:
        if isinstance(transaction["Номер карты"], str) and transaction["Номер карты"].startswith("*"):
            last_digits = transaction["Номер карты"][-4:]
            if last_digits not in cards_data:
                cards_data[last_digits] = {"last_digits": last_digits, "total_spent": 0.0, "cashback": 0.0}
        if transaction["Сумма операции"] < 0:
            cards_data[last_digits]["total_spent"] += round(transaction["Сумма операции"] * -1, 1)
            cards_data[last_digits]["cashback"] += transaction.get("Бонусы (включая кэшбэк)", 0.0)
    return list(cards_data.values())


def top_transactions(transactions: List[dict]) -> List[dict]:
    """Функция возвращает топ 5 транзакций"""
    sorted_top_5 = {}
    transactions = list(transactions.to_dict(orient="records"))
    transactions.sort(key=lambda x: x["Сумма операции"], reverse=True)
    top_5_transactions = transactions[:5]
    print(top_5_transactions)
    for transaction in top_5_transactions:
        sorted_top_5["date"] = transaction["Дата платежа"]
        sorted_top_5["amount"] = transaction["Сумма платежа"]
        sorted_top_5["category"] = transaction["Категория"]
        sorted_top_5["description"] = transaction["Описание"]
    return sorted_top_5


def main_page() -> None:
    """
    Главная функция программы, запускающая все функции модулей.
    """
    current_date = datetime.now()
    user_input = input(
        "Введите дату и время в формате YYYY-MM-DD HH:MM:SS или нажмите Enter:"
    )
    greetings = greeting(user_input if user_input else current_date)
    transactions = read_excel(FILE_PATH_EXCEL)
    total_expenses = sum_expenses_transactions(transactions)
    card_data = cards(transactions)
    top_trans = top_transactions(transactions)
    currency_rates = exchange_rate()
    stock_prices = price_stocks()

    output_data = {
        "greeting": greetings,
        "total_expenses": total_expenses,
        "card_data": card_data,
        "top_transactions": top_trans,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    output_file = "operations_data.json"
    write_json(output_file, output_data)
    print(read_json(output_file))
    #print(output_data)

if __name__ == "__main__":
    main_page()
