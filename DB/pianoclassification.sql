DROP SCHEMA IF EXISTS pianoclassification;
CREATE DATABASE IF NOT EXISTS pianoclassification
DEFAULT CHARACTER SET 'utf8mb4'
DEFAULT COLLATE 'utf8mb4_general_ci';
USE pianoclassification;

DROP TABLE ttm;
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

DROP TABLE Obra;
CREATE TABLE Obra(
	name VARCHAR(100),
    epoca Varchar (50), 
    compositor VARCHAR(100),
    piano_roll VARCHAR(500),
    descriptors FLOAT,
    time BIGINT
    
);

DROP TABLE Partitura;
CREATE TABLE Partitura(
	pdf_path VARCHAR(200),
    name VARCHAR(100),
    
    FOREIGN KEY (name) REFERENCES Obra(name),
    PRIMARY KEY (pdf_path)
);

DROP TABLE Video;
CREATE TABLE Video(
	youtube_path VARCHAR(200),
    name VARCHAR(100),
    
    FOREIGN KEY (name) REFERENCES Obra(name),
    PRIMARY KEY (youtube_path)
);

CREATE INDEX idx_name ON Video(name);

CREATE TABLE Users(
	ID INT NOT NULL AUTO_INCREMENT,
	email VARCHAR(200),

	PRIMARY KEY (ID)
);

DROP TABLE Ranking;
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


