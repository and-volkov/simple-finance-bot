from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from typing import List


class MainMenu:
    def __init__(self):
        self.resize_keyboard: bool = True
        self.one_time_keyboard: bool = False
        self.row_width: int = 2
        self.button4 = KeyboardButton(text='Help')
        self.button3 = KeyboardButton(text='Stats')
        self.button2 = KeyboardButton(text='Income')
        self.button1 = KeyboardButton(text='Expense')

    def buttons(self) -> List:
        button_list = [self.button1, self.button2,
                       self.button3, self.button4]
        return list(button_list)

    def keyboard(self) -> ReplyKeyboardMarkup:
        keys_list = self.buttons()
        keys = ReplyKeyboardMarkup(
            row_width=self.row_width,
            resize_keyboard=self.resize_keyboard).add(*keys_list)
        return keys
