--
-- Estructura BD
--

-- Crear la taula categories
CREATE TABLE categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	slug TEXT UNIQUE
);

-- Crear la taula users
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	email TEXT UNIQUE,
	password TEXT,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	updated DATETIME NOT NULL DEFAULT (DATETIME('now'))

);

-- Crear la taula products
CREATE TABLE products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT,
	description TEXT,
	photo TEXT,
	price DECIMAL(10, 2),
	category_id INTEGER,
	seller_id INTEGER,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	updated DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY (category_id) REFERENCES categories(id),
	FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- Crear la taula orders
CREATE TABLE orders (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id INTEGER,
	buyer_id INTEGER,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	CONSTRAINT uc_product_buyer UNIQUE (product_id, buyer_id),
	FOREIGN KEY (product_id) REFERENCES products(id),
	FOREIGN KEY (buyer_id) REFERENCES users(id)
);

-- Crear la taula confirmed_orders
CREATE TABLE confirmed_orders (
	order_id INTEGER PRIMARY KEY,
	created DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY (order_id) REFERENCES orders(id)
);

--
-- Dades FAKE
--
-- Inserir dades fictícies a la taula categories
INSERT INTO categories (id, name, slug) VALUES
(1, 'Electrònica', 'electronica'),
(2, 'Roba', 'roba'),
(3, 'Joguines', 'joguines');
UPDATE SQLITE_SEQUENCE SET seq = 3 WHERE name = 'categories';


-- Inserir dades fictícies a la taula users
INSERT INTO users (id, name, email, password) VALUES
(1, 'Joan Pérez', 'joan@example.com', 'contrasenya1'),
(2, 'Anna García', 'anna@example.com', 'contrasenya2'),
(3, 'Elia Rodríguez', 'elia@example.com', 'contrasenya3');
UPDATE SQLITE_SEQUENCE SET seq = 3 WHERE name = 'users';

-- Inserir dades fictícies a la taula products
INSERT INTO products (id, title, description, photo, price, category_id, seller_id) VALUES
(1, 'Telèfon mòbil', 'Un telèfon intel·ligent d''última generació.', 'no_image.png', 599.99, 1, 1),
(2, 'Samarreta', 'Una samarreta de cotó de color blau.', 'no_image.png', 19.99, 2, 2),
(3, 'Ninot de peluix', 'Un ninot de peluix suau.', 'no_image.png', 9.99, 3, 3);
UPDATE SQLITE_SEQUENCE SET seq = 3 WHERE name = 'products';

-- Inserir dades fictícies a la taula orders
INSERT INTO orders (id, product_id, buyer_id) VALUES
(1, 1, 2),
(2, 2, 1),
(3, 3, 3);
UPDATE SQLITE_SEQUENCE SET seq = 3 WHERE name = 'orders';
