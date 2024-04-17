DROP SCHEMA IF EXISTS ttm;
CREATE DATABASE IF NOT EXISTS ttm
DEFAULT CHARACTER SET 'utf8mb4'
DEFAULT COLLATE 'utf8mb4_general_ci';
USE ttm;

CREATE TABLE Obra (
	name VARCHAR(100),
    PRIMARY KEY (name)
);

CREATE TABLE Partitura(
	id VARCHAR(200),
    name VARCHAR(100),
    FOREIGN KEY (name) REFERENCES Obra(name),
    PRIMARY KEY (id)
);

CREATE TABLE Video(
	id VARCHAR(200),
    name VARCHAR(100),
    FOREIGN KEY (name) REFERENCES Obra(name),
    PRIMARY KEY (id)
);

CREATE TABLE Users(
ID INT NOT NULL AUTO_INCREMENT,
email VARCHAR(200),
PRIMARY KEY (ID)

);

CREATE TABLE Ranking(
number INT,
PRIMARY KEY (number)
);


