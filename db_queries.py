import sqlite3
from typing import Dict, List

import os


connection = sqlite3.connect(os.path.join('db', 'finances.db'))
cursor = connection.cursor()


#  Income, expense queries
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


#  Stats queries
def get_today_stats():
    cursor.execute(
        f'SELECT SUM(amount) as summary, subcategorie, categorie '
        f'FROM expenses '
        f'WHERE date(time)=CURRENT_DATE '
        f'GROUP BY subcategorie '
        f'ORDER BY summary DESC;'
    )
    return cursor.fetchall()


def get_weekly_stats():
    cursor.execute(
        f'SELECT SUM(amount) as summary, subcategorie, categorie '
        f'FROM expenses '
        f'WHERE date(current_timestamp)>=DATE("now", "weekday 0", "-7 days") '
        f'GROUP BY subcategorie '
        f'ORDER BY summary DESC '
        f'LIMIT 10;'
    )
    return cursor.fetchall()


def get_monthly_stats():
    cursor.execute(
        f'SELECT SUM(amount) as summary, subcategorie, categorie '
        f'FROM expenses '
        f'WHERE DATE(time, "start of month")=DATE("now", "start of month") '
        f'GROUP BY subcategorie '
        f'ORDER BY summary DESC '
        f'LIMIT 10'
    )
    return cursor.fetchall()


def get_top_ten_stats():
    cursor.execute(
        f'SELECT SUM(amount) as summary, subcategorie, categorie '
        f'FROM expenses '
        f'GROUP BY subcategorie '
        f'ORDER BY summary DESC '
        f'LIMIT 10;'
    )
    return cursor.fetchall()


stats_dict = {
    'Today': get_today_stats(),
    'Week': get_weekly_stats(),
    'Month': get_monthly_stats(),
    'AllTime': get_top_ten_stats()
}


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
