/*
Queries to create financial tracker database
*/

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	email VARCHAR(225) UNIQUE NOT NULL
);

CREATE TABLE category (
	category_id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL,
	user_id INT NOT NULL REFERENCES users(user_id)
);

CREATE TABLE type (
	type_id SERIAL PRIMARY KEY,
	name VARCHAR(50) NOT NULL UNIQUE CHECK (name IN ('Income', 'Expense'))
);

CREATE TABLE transactions (
	transaction_id SERIAL PRIMARY KEY,
	date DATE NOT NULL,
	description text,
	amount NUMERIC(12,2) NOT NULL,
	user_id INT NOT NULL REFERENCES users(user_id),
	category_id INT NOT NULL REFERENCES category(category_id),
	type_id INT NOT NULL REFERENCES type(type_id)
);

--Populate two possible types into Type table
INSERT INTO type (name)
VALUES 
	('Expense'),
	('Income');