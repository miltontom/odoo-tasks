-- CREATE TABLE players (
-- 	id INT PRIMARY KEY,
-- 	name VARCHAR(255),
-- 	age INT,
-- 	goals INT,
-- 	club_id INT,
-- 	country_id INT
-- );

-- CREATE TABLE club (
-- 	id INT PRIMARY KEY,
-- 	name VARCHAR(255),
-- 	coach_id INT,
-- 	country_id INT
-- );

-- CREATE TABLE coach (
-- 	id INT PRIMARY KEY,
-- 	name VARCHAR(255),
-- 	age INT,
-- 	country_id INT
-- );

-- CREATE TABLE country (
-- 	id INT PRIMARY KEY,
-- 	name VARCHAR(255)
-- );

-- INSERT INTO players VALUES (1, 'Messi', 34, 761, 901, 102);
-- INSERT INTO players VALUES (2, 'Ronaldo', 37, 801, 897, 109);
-- INSERT INTO players VALUES (3, 'Neymar', 30, 344, 901, 158);
-- INSERT INTO players VALUES (4, 'Salah', 29, 223, 635, 149);
-- INSERT INTO players VALUES (5, 'Kane', 28, 241, 975, 101);

-- INSERT INTO club VALUES (635, 'Liverpool', 7456, 101);
-- INSERT INTO club VALUES (723, 'Juventus', 2648, 136);
-- INSERT INTO club VALUES (893, 'Barcelona', 5975, 135);
-- INSERT INTO club VALUES (897, 'Manchester U.', 4821, 101);
-- INSERT INTO club VALUES (901, 'PSG', 2349, 202);
-- INSERT INTO club VALUES (975, 'Tottenham', 3414, 101);

-- INSERT INTO coach VALUES (2349, 'Pochettino', 50, 102);
-- INSERT INTO coach VALUES (2648, 'Allegri', 54, 136);
-- INSERT INTO coach VALUES (3414, 'Conte', 52, 136);
-- INSERT INTO coach VALUES (4821, 'Rangnick', 63, 124);
-- INSERT INTO coach VALUES (5975, 'Xavi', 42, 135);
-- INSERT INTO coach VALUES (7456, 'Klopp', 54, 124);

-- INSERT INTO country VALUES (101, 'England');
-- INSERT INTO country VALUES (102, 'Argentina');
-- INSERT INTO country VALUES (109, 'Portugal');
-- INSERT INTO country VALUES (124, 'Germany');
-- INSERT INTO country VALUES (135, 'Spain');
-- INSERT INTO country VALUES (136, 'Italy');
-- INSERT INTO country VALUES (149, 'Egypt');
-- INSERT INTO country VALUES (158, 'Brazil');
-- INSERT INTO country VALUES (202, 'France');

-- SELECT name as "Club"
-- FROM club
-- GROUP BY name, country_id
-- HAVING country_id = 101;

SELECT club.name
FROM club
JOIN country
ON club.country_id = country.id
WHERE country.name = 'England'

SELECT players.name as "Player", coach.name as "Coach"
FROM players
JOIN coach
ON players.country_id = coach.country_id
JOIN club
ON coach.id = club.coach_id

SELECT players.name as "Player"
FROM players
JOIN country
ON players.country_id = country.id
JOIN club
ON players.club_id = club.id and players.country_id = club.country_id

SELECT coach.name as "Coach"
FROM coach
JOIN country
ON coach.country_id = country.id

SELECT coach.name as "Coach", coach.age
FROM coach
JOIN club
ON coach.id = club.coach_id
JOIN country
ON coach.country_id = country.id and club.country_id != coach.country_id
WHERE age < 59
ORDER BY age

SELECT players.name, country.name, players.age, players.goals, club.name, coach.name
FROM players
JOIN country
ON players.country_id = country.id
JOIN club
ON club.id = players.club_id
JOIN coach
ON coach.id = club.coach_id
ORDER BY goals DESC
LIMIT 5


