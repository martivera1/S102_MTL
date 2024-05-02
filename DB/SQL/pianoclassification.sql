DROP SCHEMA IF EXISTS pianoclassification;
CREATE DATABASE IF NOT EXISTS pianoclassification
DEFAULT CHARACTER SET 'utf8mb4'
DEFAULT COLLATE 'utf8mb4_general_ci';
USE pianoclassification;

CREATE TABLE Obra(
	name VARCHAR(100),
    epoca INT, 
    compositor VARCHAR(100),
    piano_roll VARCHAR(500),
    descriptors FLOAT,
    time TIME,
    
    PRIMARY KEY (name)
);

CREATE TABLE Partitura(
	pdf_path VARCHAR(200),
    name VARCHAR(100),
    
    FOREIGN KEY (name) REFERENCES Obra(name),
    PRIMARY KEY (pdf_id)
);

CREATE TABLE Video(
	youtube_path VARCHAR(200),
    name VARCHAR(100),
    
    FOREIGN KEY (name) REFERENCES Obra(name),
    PRIMARY KEY (youtube_id)
);

CREATE TABLE Users(
	ID INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(200),

	PRIMARY KEY (ID)
);

CREATE TABLE Ranking(
	ranking INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100),
	star INT, 
	description VARCHAR(500), 
	ID INT,

	PRIMARY KEY (ranking),
	FOREIGN KEY (ID) REFERENCES Users(ID),
	FOREIGN KEY (name) REFERENCES Obra(name)
);


