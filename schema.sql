CREATE DATABASE output_db;

USE output_db;

CREATE TABLE power_data (
    premise_id INT,
    data_date VARCHAR(50),
    power_data FLOAT,
    PRIMARY KEY (premise_id, data_date)
);

CREATE TABLE predictions (
    premise_id INT,
    correlation_coefficient FLOAT,
    FOREIGN KEY (premise_id) REFERENCES power_data(premise_id)
);