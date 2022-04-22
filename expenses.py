import datetime
from typing import NamedTuple, List, Tuple

import db_queries


class Expense(NamedTuple):
    id: int
    category: str
    subcategory: str
    time: datetime.datetime
    amount: int
    description: str

    def __str__(self):
        return (
            f'Добавлен расход: {self.amount}\n'
            f'Время: {self.time}\n'
            f'Категория: {self.subcategory}:{self.category}'
            )


def add_expense(
    category: str,
    subcategory: str,
    amount: str,
) -> Expense:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = db_queries.get_expenses_description(subcategory)
    db_queries.insert(
        'expenses', {
            'categorie': category,
            'subcategorie': subcategory,
            'time': time,
            'amount': int(amount),
            'description': description
            }
        )
    return Expense(
        id=None,
        category=category,
        subcategory=subcategory,
        time=time,
        amount=amount,
        description=description
    )


def split_message(message: str):
    return message.split(',').strip()


def parse_message(message: str):
    message_list = message.split(',')
    return [val.strip() for val in message_list]


def parse_stats_query(query: List[Tuple[str]]) -> Tuple[Tuple]:
    amount, subcategorie, categorie = zip(*query)
    return amount, subcategorie, categorie


print(parse_stats_query(db_queries.get_weekly_stats()))