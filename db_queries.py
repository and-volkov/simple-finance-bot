import sqlite3
from typing import Dict, List, Tuple

import os


connection = sqlite3.connect(os.path.join('db', 'finances.db'))
cursor = connection.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join( column_values.keys() )
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    connection.commit()


def get_categories(table_name: str) -> List[str]:
    cursor.execute(
        f'SELECT categorie FROM {table_name}')
    columns = cursor.fetchall()
    return [col[0] for col in columns]


def get_subcategories(table_name: str, categorie_name) -> List[str]:
    cursor.execute(
        f'SELECT subcategorie '
        f'FROM {table_name} '
        f'WHERE categorie="{categorie_name}" '
    )
    columns = cursor.fetchall()
    return [col[0] for col in columns]


def get_expenses_description(subcategorie_name: str) -> str:
    cursor.execute(
        f'SELECT description '
        f'FROM expenses_subcategories '
        f'WHERE subcategorie="{subcategorie_name}" '
    )
    return cursor.fetchall()[0][0]


def get_income_description(categorie_name: str) -> str:
    cursor.execute(
        f'SELECT description '
        f'FROM income_categories '
        f'WHERE categorie="{categorie_name}"'
    )
    return cursor.fetchall()[0][0]


def _init_db():
    """Инициализирует БД"""
    with open("db/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    connection.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute('SELECT name FROM sqlite_master '
                   'WHERE type=\'table\' AND name=\'expenses\'')
    table_exists = cursor.fetchall()
    if not table_exists:
        _init_db()


check_db_exists()
