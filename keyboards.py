from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from typing import List

from db_queries import get_categorie_names, get_subcat_names


class Keyboard:
    def __init__(self, button_names: List[str]):
        self.button_names = button_names
        self.resize_keyboard: bool = True
        self.one_time_keyboard: bool = True
        self.row_width: int = 2

    def create_buttons(self) -> List[KeyboardButton]:
        buttons_list = []
        for button_name in self.button_names:
            buttons_list.append(KeyboardButton(text=button_name))
        return buttons_list

    def create_keyboard(self) -> ReplyKeyboardMarkup:
        keys_list = self.create_buttons()
        keyboard = ReplyKeyboardMarkup(
            row_width=self.row_width,
            resize_keyboard=self.resize_keyboard,
            one_time_keyboard=self.one_time_keyboard).add(*keys_list)
        return keyboard


class MainMenu(Keyboard):
    def __init__(self):
        button_names = ['Expense', 'Income', 'Amount', 'Stats']
        super().__init__(button_names)


class Categories(Keyboard):
    def __init__(self):
        button_names = get_categorie_names('categories', 'categorie')
        super().__init__(button_names)


class HomeSubcategories(Keyboard):
    def __init__(self):
        button_names = get_subcat_names('subcategories',
                                        'Home')
        super().__init__(button_names)


class GroceriesSubcategories(Keyboard):
    def __init__(self):
        button_names = get_subcat_names('subcategories',
                                        'Groceries')
        super().__init__(button_names)


class RestaurantsSubcategories(Keyboard):
    def __init__(self):
        button_names = get_subcat_names('subcategories',
                                        'Restaurants')
        super().__init__(button_names)


class SportSubcategories(Keyboard):
    def __init__(self):
        button_names = get_subcat_names('subcategories',
                                        'Sport')
        super().__init__(button_names)


class ClothesSubcategories(Keyboard):
    def __init__(self):
        button_names = get_subcat_names('subcategories',
                                        'Clothes')
        super().__init__(button_names)


class TravelSubcategories(Keyboard):
    def __init__(self):
        button_names = get_subcat_names('subcategories',
                                        'Travel')
        super().__init__(button_names)
