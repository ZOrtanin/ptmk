import subprocess
import pytest
import re

# Путь к твоей программе
APP_PATH = "python main.py"


def test_mode_1_create_table():
    """Тест для режима 1: Создание таблицы."""
    result = subprocess.run(
        f"{APP_PATH} 1",
        shell=True,
        capture_output=True,
        text=True
    )
    assert "The database has been successfully created" in result.stdout, f"Ошибка: {result.stderr}"


def test_mode_2_1_add_employee():
    """Тест для режима 2: Добавление сотрудника."""
    result = subprocess.run(
        f'{APP_PATH} 2 "Ivanov Petr Sergeevich" 2009-07-12 Male',
        shell=True,
        capture_output=True,
        text=True
    )
    assert "1 line added" in result.stdout, f"Ошибка: {result.stderr}"


def test_mode_2_2_add_employee():
    """Тест для режима 2: Добавление нескольких сотрудников."""
    result = subprocess.run(
        f'{APP_PATH} 2 "Ivanov Petr Sergeevich" 2009-07-12 Male "Petrov Ivan Sergeevich" 2009-07-12 Male',
        shell=True,
        capture_output=True,
        text=True
    )
    assert "2 lines added" in result.stdout, f"Ошибка: {result.stderr}"


def test_mode_3_list_employees():
    """Тест для режима 3: Вывод всех сотрудников."""
    result = subprocess.run(
        f"{APP_PATH} 3",
        shell=True,
        capture_output=True,
        text=True
    )
    assert "Ivanov Petr Sergeevich" in result.stdout, f"Ошибка: {result.stderr}"
    assert "2009-07-12" in result.stdout, f"Ошибка: {result.stderr}"
    assert "Male" in result.stdout, f"Ошибка: {result.stderr}"


def test_mode_4_bulk_insert():
    """Тест для режима 4: Массовое заполнение 1000000 записей."""
    import time
    start_time = time.time()
    result = subprocess.run(
        f"{APP_PATH} 4 0",
        shell=True,
        capture_output=True,
        text=True
    )
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Bulk insert time: {execution_time:.2f} seconds")
    assert execution_time < 60, "Время выполнения превышает 60 секунд"


def test_mode_5_query_by_criteria():
    """Тест для режима 5: Выборка по критерию (мужчины, фамилия на F)."""
    result = subprocess.run(
        f"{APP_PATH} 5",
        shell=True,
        capture_output=True,
        text=True
    )
    assert "seconds spent on request execution" in result.stdout, f"Ошибка: {result.stderr}"
    # Проверяем, что в выводе есть мужчины с фамилией на F
    assert re.search(r"ФИО: F\w+ \w+ \w+, Дата рождения: \d{4}-\d{2}-\d{2}, Пол: Male, кол-во полных лет: \d+", result.stdout), f"Ошибка: {result.stderr}"
