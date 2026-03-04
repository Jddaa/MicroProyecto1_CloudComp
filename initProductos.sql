
CREATE DATABASE IF NOT EXISTS productos;
use productos;

CREATE TABLE products (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name varchar(255),
    description text,
    price decimal(10,2),
    stock int
);

INSERT INTO products VALUES(null, "Manguera Inalambrica", null, 1500, 25),
    (null, "Aceite en Polvo", null, 2500, 30);

