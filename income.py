import datetime
from typing import NamedTuple

import db_queries


class Income(NamedTuple):
    id: int
    amount: int
    time: datetime.datetime
    income_categorie: str
    income_description: str

    def __str__(self):
        return (
            f'Добавлено {self.amount}  рублей\n'
            f'Время: {self.time}\n'
            f'В категорию {self.income_categorie}:'
            f'{self.income_description}'
        )


def add_income(amount: int, income_categorie: str):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    description = db_queries.get_income_description(income_categorie)
    inserted_row_id = db_queries.insert(
        'income', {
            'amount': amount,
            'time': time,
            'income_categorie': income_categorie,
            'income_description': description
        }
    )
    return Income(
        id=None,
        amount=int(amount),
        time=time,
        income_categorie=income_categorie,
        income_description=description
    )
