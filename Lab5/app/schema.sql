DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    description TEXT
) ENGINE INNODB;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(25) UNIQUE NOT NULL,
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    middle_name VARCHAR(25) DEFAULT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id)
) ENGINE INNODB;

CREATE TABLE visit_logs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    path VARCHAR(100) UNIQUE NOT NULL,
    user_id INTEGER DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE INNODB;

-- INSERT INTO roles (name) VALUES ('admin')
-- INSERT INTO roles (name) VALUES ('another_role')
-- INSERT INTO users (username, first_name, last_name, password_hash, role_id) VALUES ('admin', 'adminFN', 'adminLN', SHA2('qwerty', 256), 1)