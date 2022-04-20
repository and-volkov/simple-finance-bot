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


def add_transaction(
        category: str,
        subcategory: str,
        amount: str,
        description: str) -> Transaction:
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inserted_row_id = db_queries.insert(
        'transactions', {
            'category_name': category,
            'subcategory_name': subcategory,
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
