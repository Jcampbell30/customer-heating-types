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

CREATE TABLE anomaly_types (
    anomaly_type_id INT,
    anomaly_type varchar(50),
    anomaly_desc varchar(50),
    PRIMARY KEY (anomaly_type_id)
);

INSERT INTO anomaly_types(anomaly_type_id, anomaly_type, anomaly_desc) VALUES (1, "Zero-Usage", "A premise that's data shows zero electrical usage for a given period.");
INSERT INTO anomaly_types(anomaly_type_id, anomaly_type, anomaly_desc) VALUES (2, "Negative-Usage", "A premise that's data shows negative electrical usage for a given period.");
INSERT INTO anomaly_types(anomaly_type_id, anomaly_type, anomaly_desc) VALUES (3, "Non-Confidence", "A premise that's data assessment shows an unacceptable level of confidence.");

CREATE TABLE anomalies (
    id INT NOT NULL AUTO_INCREMENT,
    premise_id INT,
    data_date VARCHAR(50),
    anomaly_type_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (premise_id) REFERENCES power_data(premise_id),
    FOREIGN KEY (data_date) REFERENCES power_data(data_date),
    FOREIGN KEY (anomaly_type_id) REFERENCES anomaly_types(anomaly_type_id)
);