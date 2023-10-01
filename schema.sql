CREATE DATABASE output_db;

CREATE TABLE weather(
    data_date VARCHAR(50),
    temp FLOAT,
    PRIMARY KEY (data_date)
);

CREATE TABLE power_data (
    premise_id INT,
    data_date VARCHAR(50),
    power_data FLOAT,
    FOREIGN KEY (data_date) REFERENCES weather(data_date),
    PRIMARY KEY (premise_id, data_date)
);

CREATE TABLE predictions (
    premise_id INT,
    correlation_coefficient FLOAT,
    FOREIGN KEY (premise_id) REFERENCES power_data(premise_id)
);