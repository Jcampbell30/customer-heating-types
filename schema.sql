CREATE DATABASE output_db;

CREATE TABLE output_data (
    premise_id INT,
    data_date VARCHAR(50),
    weather_data FLOAT,
    power_data FLOAT,
    PRIMARY KEY (premise_id, data_date)
);