-- Crear la taula categories
CREATE TABLE categories (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE,
	slug VARCHAR(255) NOT NULL UNIQUE
);

-- Crear la taula statuses
CREATE TABLE statuses (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) UNIQUE,
	slug VARCHAR(255) UNIQUE
);

-- Crear la taula users
CREATE TABLE users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE,
	email VARCHAR(255) NOT NULL UNIQUE,
	role VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	email_token VARCHAR(255) DEFAULT NULL,
	verified TINYINT NOT NULL DEFAULT 0, -- MySQL utilitza TINYINT per a booleans
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	token VARCHAR(32) UNIQUE,
	token_expiration DATETIME DEFAULT NULL,
	INDEX (token) -- INDEX ha de ser fora de la declaració de la columna
);

-- Crear la taula products
CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
	description TEXT NOT NULL,
	photo VARCHAR(255) NOT NULL,
	price DECIMAL(10, 2) NOT NULL,
	category_id INT NOT NULL,
	status_id INT NOT NULL,
	seller_id INT NOT NULL,
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (category_id) REFERENCES categories(id),
	FOREIGN KEY (status_id) REFERENCES statuses(id),
	FOREIGN KEY (seller_id) REFERENCES users(id)
);

-- Crear la taula blocked_users
CREATE TABLE blocked_users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT NOT NULL,
	admin_id INT NOT NULL,
	message VARCHAR(255) NOT NULL,
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Crear la taula orders
CREATE TABLE orders (
	id INT AUTO_INCREMENT PRIMARY KEY,
	product_id INT,
	buyer_id INT,
	offer DECIMAL(10, 2),
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	UNIQUE KEY uc_product_buyer (product_id, buyer_id),
	FOREIGN KEY (product_id) REFERENCES products(id),
	FOREIGN KEY (buyer_id) REFERENCES users(id)
);

-- Crear la taula confirmed_orders
CREATE TABLE confirmed_orders (
	order_id INT AUTO_INCREMENT PRIMARY KEY,
	created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (order_id) REFERENCES orders(id)
);
