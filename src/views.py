import json
from datetime import datetime
from typing import List

from config import FILE_PATH_EXCEL
from src.utils import exchange_rate, greeting, price_stocks, read_excel


def sum_expenses_transactions(transactions: List[dict]) -> float:
    """Функция возвращает сумму расходов по списку"""
    transactions = list(transactions.to_dict(orient="records"))
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
    transactions = list(transactions.to_dict(orient="records"))
    transactions.sort(key=lambda x: x["Сумма операции"], reverse=True)
    top_5_transactions = transactions[:5]
    sorted_top_5 = [
            {
                "date": t["Дата платежа"],
                "amount": t["Сумма операции с округлением"],
                "category": t["Категория"],
                "description": t["Описание"]
            }
            for t in top_5_transactions
            ]
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
        "cards": card_data,
        "top_transactions": top_trans,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }
    json_output_data = json.dumps(output_data, indent=4, ensure_ascii=False)

    return json_output_data


if __name__ == "__main__":
    print(main_page())
