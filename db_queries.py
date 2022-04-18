import sqlite3
from typing import Dict, List, Tuple

import os


connection = sqlite3.connect(os.path.join('db', 'finances.db'))
cursor = connection.cursor()


def get_categorie_names(table_name: str, cat_name) -> List[str]:
    cursor.execute(f'SELECT {cat_name} FROM {table_name}')
    columns = cursor.fetchall()
    return [col[0] for col in columns]


def get_subcat_names(table_name: str, cat_name: str) -> List[str]:
    cursor.execute(f'SELECT subcategorie_name '
                   f'FROM {table_name} '
                   f'WHERE categorie_name = "{cat_name}"')
    columns = cursor.fetchall()
    return [col[0] for col in columns]


def _init_db():
    """Инициализирует БД"""
    with open("db/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    connection.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute('SELECT name FROM sqlite_master '
                   'WHERE type=\'table\' AND name=\'categories\'')
    table_exists = cursor.fetchall()
    if not table_exists:
        _init_db()


check_db_exists()
