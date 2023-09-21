CREATE DATABASE output_db;

CREATE TABLE power_data (
    premise_id INT,
    data_date VARCHAR(50),
    power_data FLOAT,
    PRIMARY KEY (premise_id, data_date)
);

CREATE TABLE weather(
    data_date VARCHAR(50),
    temp FLOAT,
    PRIMARY KEY (data_date)
);