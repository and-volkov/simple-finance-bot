import datetime
from typing import NamedTuple

import db_queries


class Income(NamedTuple):
    id: int
    amount: int
    time: datetime.datetime
    categorie: str
    description: str

    def __str__(self):
        return (
            f'Добавлено {self.amount}  рублей\n'
            f'Время: {self.time}\n'
            f'В категорию {self.categorie}:'
            f'{self.description}'
        )


def add_income(amount: int, categorie: str):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = db_queries.get_income_description(categorie)
    db_queries.insert(
        'income', {
            'amount': amount,
            'time': time,
            'categorie': categorie,
            'description': description
            }
        )
    return Income(
        id=None,
        amount=int(amount),
        time=time,
        categorie=categorie,
        description=description
    )
