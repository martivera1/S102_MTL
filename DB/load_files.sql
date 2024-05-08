USE pianoclassification;

LOAD DATA INFILE 'cleaned_data_new.csv'
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

#INSERT IGNORE INTO Partitura (name)
#SELECT DISTINCT name FROM Obra
#;


select @@datadir;
select *from ranking;