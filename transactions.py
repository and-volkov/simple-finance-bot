import datetime
from typing import NamedTuple

import db_queries


class Transaction(NamedTuple):
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


def add_transaction(
        category: str,
        subcategory: str,
        amount: str,
        description: str) -> Transaction:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inserted_row_id = db_queries.insert(
        'transactions', {
            'categorie_name': category,
            'subcategorie_name': subcategory,
            'time': time,
            'amount': int(amount),
            'description': description
        }
    )
    return Transaction(
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

print()
