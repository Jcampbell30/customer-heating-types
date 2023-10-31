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

CREATE TABLE anomalies (
    premise_id INT,
    data_date VARCHAR(50),
    anomaly_id INT,
    FOREIGN KEY (premise_id) REFERENCES power_data(premise_id),
    FOREIGN KEY (data_date) REFERENCES power_data(data_date),
    FOREIGN KEY (anomaly_id) REFERENCES anomaly_types(anomaly_id)
);

CREATE TABLE anomaly_types (
    anomaly_id INT,
    anomaly_type varchar(50),
    anomaly_desc varchar(50),
    PRIMARY KEY (anomaly_id)
);
