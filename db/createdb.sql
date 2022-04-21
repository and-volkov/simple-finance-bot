DROP TABLE IF EXISTS transactions;
CREATE TABLE expenses(
	id INTEGER primary key,
	categorie VARCHAR(255) REFERENCES categories(categorie),
	subcategorie VARCHAR(255) REFERENCES subcategories(subcategorie_name),
	time DATETIME,
	amount INTEGER,
	description TEXT
	);

CREATE TABLE expenses_categories(
	categorie VARCHAR(255) PRIMARY KEY,
	description VARCHAR(255)
	);

DROP TABLE IF EXISTS expenses_subcategories;
CREATE TABLE expenses_subcategories(
    subcategorie VARCHAR(255) PRIMARY KEY,
    categorie VARCHAR(255) REFERENCES categories(categorie),
    description VARCHAR(255),
    commentary TEXT
);

DROP TABLE IF EXISTS income;
CREATE TABLE income(
	id INTEGER PRIMARY KEY,
	amount INTEGER,
	time DATETIME,
	categorie VARCHAR(255),
	description VARCHAR(255)
	);

DROP TABLE IF EXISTS income_categories;
CREATE TABLE income_categories(
    id INTEGER PRIMARY KEY,
    categorie VARCHAR(255) REFERENCES  income(categorie),
    description VARCHAR (255) REFERENCES income(description)
);

INSERT INTO expenses_categories(categorie, description)
	VALUES
	("Home", "Дом"),
	("Groceries", "Продукты"),
	("Restaurants", "Рестораны"),
	("Sport", "Спорт"),
	("Clothes", "Одежда"),
	("Travel", "Поездки");

INSERT INTO expenses_subcategories(subcategorie, categorie, description)
    VALUES
    /* Insert for Home categorie */
    ("Water", "Home", "Вода"),
    ("Electricity", "Home", "Электричество"),
    ("Internet", "Home", "Интернет"),
    ("Chemicals", "Home", "Бытовая Химия"),
    ("Medicine", "Home", "Лекарства"),
    ("Subscriptions", "Home", "Подписки"),
    ("Other-Home", "Home", "Другое"),
    /* Insert for Groceries category */
    ("Meat", "Groceries", "Мясо"),
    ("Carbs", "Groceries", "Углеводы"),
    ("Vegetables", "Groceries", "Овощи"),
    ("Fruits", "Groceries", "Фрукты"),
    ("Milk", "Groceries", "Молочка"),
    ("Drinks", "Groceries", "Напитки"),
    ("Sweets", "Groceries", "Сладкое"),
    ("Other-Groceries", "Groceries", "Другое"),
    /* Insert for Restaurants category */
    ("Dinner", "Restaurants", "Ужин"),
    ("Lunch", "Restaurants", "Обед"),
    ("Breakfast", "Restaurants", "Завтрак"),
    ("Coffe", "Restaurants", "Кофе"),
    ("Other-Restaurants", "Restaurants", "Другое"),
    /* Insert for Sport category */
    ("Subscription", "Sport", "Абонемент"),
    ("Nutrition", "Sport", "Спорт-пит"),
    ("Vitamins", "Sport", "Витамины"),
    ("Other-Sport", "Sport", "Другое"),
    /* Insert for Clothes category */
    ("Shoes", "Clothes", "Обувь"),
    ("T-shirts", "Clothes", "Футболки"),
    ("Pants", "Clothes", "Штаны"),
    ("Underwear", "Clothes", "Нижнее Белье"),
    ("Outerwear", "Clothes", "Верхняя Одежда"),
    ("Shirts/hoodies", "Clothes", "Рубашки, Балахоны"),
    ("Sportswear", "Clothes", "Спортивная одежда"),
    ("Other-Clothes", "Clothes", "Другое"),
    /* Insert for Travel category */
    ("Flights", "Travel", "Перелеты"),
    ("Trains", "Travel", "Поезд"),
    ("Accommodation", "Travel", "Проживание"),
    ("Transfer", "Travel", "Переезд"),
    ("Other-Travel", "Travel", "Другое");

INSERT INTO income_categories(categorie, description)
    VALUES
    ("Salary", "Зарплата"),
    ("Bonus", "Премия"),
    ("Freelance", "Подработка"),
    ("Other", "Другое");