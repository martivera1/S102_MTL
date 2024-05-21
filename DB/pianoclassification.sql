DROP SCHEMA IF EXISTS pianoclassification;
CREATE DATABASE IF NOT EXISTS pianoclassification
DEFAULT CHARACTER SET 'utf8mb4'
DEFAULT COLLATE 'utf8mb4_general_ci';
USE pianoclassification;

DROP TABLE IF EXISTS ttm;
CREATE TABLE ttm (
	surname VARCHAR (1000) NOT NULL,
    firstname VARCHAR (100) NOT NULL ,
    music VARCHAR (900) NOT NULL,
    nationality VARCHAR (100),
    birth varchar(50),
    death varchar(50), 
    youtube_title VARCHAR (1000) NOT NULL,
    youtube_id VARCHAR (100) NOT NULL,
    audio_name VARCHAR (500),
    audio_duration BIGINT
);

DROP TABLE IF EXISTS Obra;
CREATE TABLE Obra(
	id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    epoca Varchar (50), 
    compositor VARCHAR(100),
    piano_roll VARCHAR(500),
    descriptors FLOAT,
    time BIGINT,
    PRIMARY KEY (id)
);

DROP TABLE IF EXISTS Partitura;
CREATE TABLE Partitura(
	id INT NOT NULL AUTO_INCREMENT,
	pdf_path VARCHAR(200),
    name VARCHAR(100),
    
    FOREIGN KEY (id) REFERENCES Obra(id),
    PRIMARY KEY (pdf_path)
);

DROP TABLE IF EXISTS Video;
CREATE TABLE Video(
	id INT NOT NULL AUTO_INCREMENT,
	youtube_path VARCHAR(200),
    name VARCHAR(100),
    
    FOREIGN KEY (id) REFERENCES Obra(id),
    PRIMARY KEY (youtube_path)
);

CREATE INDEX idx_name ON Video(name);

DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
	IDranking INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(200),

	PRIMARY KEY (ID)
);

DROP TABLE IF EXISTS Ranking;
CREATE TABLE Ranking(
	ranking INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100),
	star INT, 
	description VARCHAR(500), 
	ID INT,

	PRIMARY KEY (ranking),
	FOREIGN KEY (ID) REFERENCES Users(ID),
	FOREIGN KEY (ID) REFERENCES Obra(id)
);


