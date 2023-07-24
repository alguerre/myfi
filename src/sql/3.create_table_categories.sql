DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT
);

INSERT INTO categories (category)
VALUES ('ALQUILER'),
       ('PISO'),
       ('COMIDA'),
       ('DEPORTE'),
       ('EFECTIVO'),
       ('FACTURA'),
       ('TRANSPORTE'),
       ('OTROS'),
       ('RESTAURANTE'),
       ('UNKNOWN'),
       ('N26');