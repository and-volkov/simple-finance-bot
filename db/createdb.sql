DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions(
	id INTEGER primary key,
	categorie_name VARCHAR(255) REFERENCES categories(categorie),
	subcategorie_name VARCHAR(255) REFERENCES subcategories(subcategorie_name),
	time DATETIME,
	amount INTEGER,
	description TEXT
	);

CREATE TABLE categories(
	categorie VARCHAR(255) PRIMARY KEY,
	categorie_desc VARCHAR(255)
	);

DROP TABLE IF EXISTS subcategories;
CREATE TABLE subcategories(
    subcategorie_name VARCHAR(255) PRIMARY KEY,
    categorie_name VARCHAR(255) REFERENCES categories(categorie),
    subcategorie_desc VARCHAR(255),
    commentary TEXT
);

DROP TABLE IF EXISTS income;
CREATE TABLE income(
	id INTEGER PRIMARY KEY,
	amount INTEGER,
	time DATETIME,
	source VARCHAR(255),
    income_categorie VARCHAR(255)
	);

DROP TABLE IF EXISTS income_categories;
CREATE TABLE income_categories(
    id INTEGER PRIMARY KEY,
    income_categorie_name VARCHAR(255) REFERENCES  income(income_categorie),
    income_description TEXT
);

INSERT INTO categories(categorie, categorie_desc)
	VALUES
	("Home", "Дом"),
	("Groceries", "Продукты"),
	("Restaurants", "Рестораны"),
	("Sport", "Спорт"),
	("Clothes", "Одежда"),
	("Travel", "Поездки");

INSERT INTO subcategories(subcategorie_name, categorie_name, subcategorie_desc)
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

INSERT INTO income_categories(income_categorie_name, income_description)
    VALUES
    ("Salary", "Зарплата"),
    ("Bonus", "Премия"),
    ("Freelance", "Подработка"),
    ("Other", "Другое");
