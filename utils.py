"""Вспомогательные функции для безопасного ввода данных."""

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с повторением при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print('Ошибка: введите целое число.')


def input_date(prompt: str) -> date:
    """Запросить у пользователя дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt), '%d.%m.%Y').date()
        except ValueError:
            print('Ошибка: введите дату в формате ДД.ММ.ГГГГ.')