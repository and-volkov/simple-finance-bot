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


def get_income_description(cat_name: str) -> str:
    table_name = 'income_categories'
    cursor.execute(
        f'SELECT income_description_name '
        f'FROM {table_name} ' 
        f'WHERE income_categorie_name = "{cat_name}"'
    )
    return cursor.fetchall()[0][0]


def get_categorie_by_subcategorie(sub_cat_name: str) -> str:
    table_name = 'subcategories'
    cursor.execute(
        f'SELECT categorie_name '
        f'FROM {table_name} '
        f'WHERE subcategorie_name = "{sub_cat_name}"'
    )
    return cursor.fetchall()[0][0]


def select_all_categories():
    table_name = 'categories'
    cursor.execute(
        f'SELECT DISTINCT categorie '
        f'FROM {table_name} '
    )
    categories = cursor.fetchall()
    cat_list = [cat[0] for cat in categories]
    return cat_list


def select_all_subcategories():
    table_name = 'subcategories'
    cursor.execute(
        f'SELECT DISTINCT subcategorie_name '
        f'FROM {table_name} '
    )
    subcategories = cursor.fetchall()
    sub_list = [sub_cat[0] for sub_cat in subcategories]
    return sub_list


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
