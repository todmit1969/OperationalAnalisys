import json
import logging
from unittest.mock import patch

import pytest

from src.services import cash_by_category

logging.basicConfig(level=logging.INFO)


@pytest.fixture
def transactions():
    return [
        {"date": "2023-10-01", "Бонусы (включая кэшбэк)": -1500, "Категория": "Одежда и обувь"},
        {"date": "2023-10-05", "Бонусы (включая кэшбэк)": -2000, "Категория": "Супермаркеты"},
        {"date": "2023-10-10", "Бонусы (включая кэшбэк)": -3000, "Категория": "Фастфуд"},
        {"date": "2023-10-12", "Бонусы (включая кэшбэк)": -1000, "Категория": "Косметика"},
        {"date": "2023-09-15", "Бонусы (включая кэшбэк)": -500, "Категория": "Еда"},
    ]


@patch("logging.getLogger")
def test_cash_by_category(mock_logger, transactions):
    """Тестируем получение выгодных категорий кешбэка."""
    result = cash_by_category(transactions)

    expected_result = {
        "Одежда и обувь": 26,
        "Супермаркеты": 146,
        "Фастфуд": 110,
        "Косметика": 7,
    }
    assert json.loads(result) == expected_result  # Проверяем результат