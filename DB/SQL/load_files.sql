USE ttm;

LOAD DATA INFILE 'cleaned_data.csv'
INTO TABLE ttm
COLUMNS TERMINATED BY ';' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

select * from obra;

select @@datadir;