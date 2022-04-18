import sqlite3
from typing import Dict, List, Tuple

import os


connection = sqlite3.connect(os.path.join('db', 'finances.db'))
cursor = connection.cursor()


def get_columns(table_name: str, name) -> List[str]:
    cursor.execute(f'SELECT {name} FROM {table_name}')
    cols = cursor.fetchall()
    return cols


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
