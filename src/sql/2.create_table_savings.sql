DROP TABLE IF EXISTS savings;

CREATE TABLE savings (
    date DATE NOT NULL,
    amount decimal(12,2) NOT NULL,
    total decimal(12,2) NOT NULL
);