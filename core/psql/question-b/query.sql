-- CREATE TABLE movie_cast (
-- 	act_id INT, 
-- 	mov_id INT,
-- 	role VARCHAR(255)
-- );

-- INSERT INTO movie_cast VALUES (101, 901, 'John Scottie Ferguson');
-- INSERT INTO movie_cast VALUES (102, 902, 'Miss Giddens');
-- INSERT INTO movie_cast VALUES (107, 907, 'Alice Harford');
-- INSERT INTO movie_cast VALUES (110, 910, 'Eddie Adams');
-- INSERT INTO movie_cast VALUES (111, 911, 'Alvy Singer');
-- INSERT INTO movie_cast VALUES (113, 913, 'Andy Dufresne');
-- INSERT INTO movie_cast VALUES (114, 914, 'Lester Burnham');
-- INSERT INTO movie_cast VALUES (115, 915, 'Rose DeWitt Bukater');
-- INSERT INTO movie_cast VALUES (120, 920, 'Elizabeth Darko');
-- INSERT INTO movie_cast VALUES (121, 921, 'Older Jamal');
-- INSERT INTO movie_cast VALUES (114, 923, 'Bobby Darin');

-- CREATE TABLE actors (
-- 	act_id INT,
-- 	act_fname VARCHAR(255),
-- 	act_lname VARCHAR(255),
-- 	act_gender VARCHAR(1)
-- );

-- INSERT INTO actors VALUES (101, 'James', 'Stewart', 'M');
-- INSERT INTO actors VALUES (102, 'Deborah', 'Kerr', 'F');
-- INSERT INTO actors VALUES (107, 'Nicole', 'Kidman', 'F');
-- INSERT INTO actors VALUES (110, 'Mark', 'Wahlberg', 'M');
-- INSERT INTO actors VALUES (111, 'Woody', 'Allen', 'M');
-- INSERT INTO actors VALUES (113, 'Tim', 'Robbins', 'M');
-- INSERT INTO actors VALUES (114, 'Kevin', 'Spacey', 'M');
-- INSERT INTO actors VALUES (115, 'Kate', 'Winslet', 'F');
-- INSERT INTO actors VALUES (120, 'Maggie', 'Gyllenhaal', 'F');
-- INSERT INTO actors VALUES (121, 'Dev', 'Patel', 'M');
-- INSERT INTO actors VALUES (123, 'David', 'Aston', 'M');
-- INSERT INTO actors VALUES (124, 'Ali', 'Astin', 'F');

-- CREATE TABLE movie (
-- 	mov_id INT,
-- 	mov_title VARCHAR(255),
-- 	mov_year INT,
-- 	mov_time INT,
-- 	mov_lang VARCHAR(255),
-- 	mov_dt_rel DATE,
-- 	mov_rel_country VARCHAR(255)
-- );

-- INSERT INTO movie
-- VALUES (901, 'Vertigo', 1958, 128, 'English', '1958-08-24', 'UK'),
-- (902, 'The Innocents', 1961, 100, 'English', '1962-02-19', 'SW'),
-- (907, 'Eyes Wide Shut', 1999, 159, 'English', NULL, 'UK'),
-- (910, 'Boogie Nights', 1997, 155, 'English', '1998-02-16', 'UK'),
-- (911, 'Annie Hall', 1977, 93, 'English', '1977-04-20', 'USA'),
-- (913, 'The Shawshank Redemption', 1994, 142, 'English', '1995-02-17', 'UK'),
-- (914, 'American Beauty', 1999, 122, 'English', NULL, 'UK'),
-- (915, 'Titanic', 1997, 194, 'English', '1998-01-23', 'UK'),
-- (920, 'Donnie Darko', 2001, 113, 'English', NULL, 'UK'),
-- (921, 'Slumdog Millionaire', 2008, 120, 'English', '2009-01-09', 'UK'),
-- (926, 'Seven Samurai', 1954, 207, 'Japanese', '1954-04-26', 'JP'),
-- (927, 'Spirited Away', 2001, 125, 'Japanese', '2003-09-12', 'UK'),
-- (928, 'Back to the Future', 1985, 116, 'English', '1985-12-04', 'UK'),
-- (925, 'Braveheart', 1995, 178, 'English', '1995-09-08', 'UK');


-- CREATE TABLE rating (
-- 	mov_id INT,
-- 	rev_id INT,
-- 	rev_stars FLOAT,
-- 	num_o_ratings BIGINT
-- );

-- INSERT INTO rating VALUES
-- 	(901, 9001, 8.40, 263575),
-- 	(902, 9002, 7.90, NULL),
-- 	(910, 9009, 3.00, 195961),
-- 	(911, 9010, 8.10, 203875),
-- 	(914, 9013, 7.00, 862618),
-- 	(915, 9001, 7.70, 81328),
-- 	(925, 9015, 7.70, 81328),
-- 	(920, 9017, 8.10, 609451),
-- 	(921, 9018, 8.00, 667758);

SELECT actors.act_fname || ' ' || actors.act_lname as "Cast"
FROM movie
JOIN movie_cast
ON movie.mov_id = movie_cast.mov_id
JOIN actors
ON actors.act_id = movie_cast.act_id
WHERE movie.mov_title = 'Slumdog Millionaire'


SELECT movie.mov_title as "Movie"
FROM movie_cast
JOIN actors
ON actors.act_id = movie_cast.act_id
JOIN movie
ON movie.mov_id = movie_cast.mov_id
WHERE actors.act_fname = 'Tim' and actors.act_lname = 'Robbins'





