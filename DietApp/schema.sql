CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    kalories INT NOT NULL,
    protein INT NOT NULL,
    fat INT NOT NULL,
    carbohydrates INT NOT NULL,
    is_public BOOLEAN,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES users(id)
) ENGINE INNODB;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(25) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    is_admin BOOLEAN
) ENGINE INNODB;

CREATE TABLE meals (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    meal_category ENUM("Breakfast", "Lunch", "Dinner"),
    kalories_total INT NOT NULL,
    protein_total INT NOT NULL,
    fat_total INT NOT NULL,
    carbohydrates_total INT NOT NULL,
    owner_id INTEGER,
    FOREIGN KEY (owner_id) REFERENCES users(id)
) ENGINE INNODB;

CREATE TABLE m2m_products_meals (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    weight INT NOT NULL,
    product_id INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(id),
    meal_id INTEGER,
    FOREIGN KEY (meal_id) REFERENCES meals(id)
)

-- INSERT INTO roles (name) VALUES ('admin')
-- INSERT INTO roles (name) VALUES ('another_role')