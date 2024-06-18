set global local_infile=1;
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
    id_obra INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    epoca Varchar (50),
    compositor VARCHAR(100),
    piano_roll VARCHAR(500),
    atr_complexity INT,
    atr_entropy FLOAT,
    atr_duration FLOAT,
    time BIGINT,
    PRIMARY KEY (id_obra)
);
DROP TABLE IF EXISTS Partitura;
CREATE TABLE Partitura(
    id_partitura INT NOT NULL AUTO_INCREMENT,
    pdf_path VARCHAR(200),
    name VARCHAR(100),
    FOREIGN KEY (id_partitura) REFERENCES Obra(id_obra),
    PRIMARY KEY (pdf_path)
);
DROP TABLE IF EXISTS Video;
CREATE TABLE Video(
    id_video INT NOT NULL AUTO_INCREMENT,
    youtube_path VARCHAR(200),
    name VARCHAR(100),
    FOREIGN KEY (id_video) REFERENCES Obra(id_obra),
    PRIMARY KEY (youtube_path)
);
CREATE INDEX idx_name ON Video(name);
DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    id_user INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(200),
    PRIMARY KEY (id_user)
);
DROP TABLE IF EXISTS Ranking;
CREATE TABLE Ranking(
    id_ranking INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    star INT,
    description VARCHAR(500),
    user_id INT,
    obra_id INT,
    PRIMARY KEY (id_ranking, obra_id),
    FOREIGN KEY (user_id) REFERENCES Users(id_user),
    FOREIGN KEY (obra_id) REFERENCES Obra(id_obra)
);

DROP TABLE IF EXISTS temp_obra;
CREATE TEMPORARY TABLE temp_obra (
    name VARCHAR(255),
    lz_complexity INT,
    pitch_entropy FLOAT,
    duration FLOAT
);

USE pianoclassification;
LOAD DATA LOCAL INFILE '/api/db/cleaned_data.csv'
INTO TABLE ttm
COLUMNS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
;
INSERT IGNORE INTO Obra(name, epoca, compositor, time)
SELECT DISTINCT youtube_id, birth, firstname, audio_duration FROM ttm;
INSERT IGNORE INTO Video(youtube_path, name)
SELECT DISTINCT youtube_id, music FROM ttm;
INSERT IGNORE INTO Partitura( name)
SELECT DISTINCT music FROM ttm;
-- INSERT IGNORE INTO Partitura (name)
-- SELECT DISTINCT name FROM Obra
USE pianoclassification;
LOAD DATA LOCAL INFILE '/api/db/features.csv'
INTO TABLE temp_obra
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(name, lz_complexity, pitch_entropy, duration);
UPDATE Obra o
INNER JOIN temp_obra t ON o.name = t.name
SET 
    o.atr_complexity = t.lz_complexity,
    o.atr_entropy = t.pitch_entropy,
    o.atr_duration = t.duration;

DELETE FROM Video
WHERE id_video IN (
    SELECT id_obra
    FROM obra
    WHERE atr_complexity IS NULL
       OR atr_entropy IS NULL
);
DELETE FROM Obra
WHERE atr_complexity IS NULL
   OR atr_entropy IS NULL;
