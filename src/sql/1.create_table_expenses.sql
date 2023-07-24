DROP TABLE IF EXISTS finances;

CREATE TABLE finances (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    concept TEXT,
    amount decimal(12,2) NOT NULL,
    total decimal(12,2) NOT NULL,
    category TEXT,
    automatic BOOLEAN,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_on TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_on = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_modtime
    BEFORE UPDATE ON finances
    FOR EACH ROW EXECUTE PROCEDURE  update_modified_column();