CREATE TABLE transactions(
	id INTEGER primary key,
	categorie_name VARCHAR(255) REFERENCES categories(categorie_pk),
	amount INTEGER,
	time DATETIME,
	description TEXT
	);

CREATE TABLE categories(
	categorie_pk VARCHAR(255) PRIMARY KEY,
	categorie_desc VARCHAR(255)
	);

CREATE TABLE income(
	id INTEGER PRIMARY KEY,
	amount INTEGER,
	time DATETIME,
	source VARCHAR(255)
	);

INSERT INTO categories(categorie_pk, categorie_desc)
	VALUES
	("Home", "Дом"),
	("Groceries", "Продукты"),
	("Cigarettes", "Сигареты"),
	("Coffe", "Кофе"),
	("Restaurants", "Рестораны"),
	("Sport", "Спорт"),
	("Clothes", "Одежда"),
	("Subscriptions", "Подписки"),
	("Other", "Другое");
