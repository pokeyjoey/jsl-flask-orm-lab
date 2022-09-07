DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS movie_actors;
DROP TABLE IF EXISTS movie_directors;
DROP TABLE IF EXISTS directors;

CREATE TABLE movies (
  id serial primary key,
  title varchar(250),
  studio varchar(250),
  runtime REAL,
  description text,
  release_date varchar(250),
  year INTEGER
);

CREATE TABLE actors (
  id serial primary key,
  name varchar(250)
);

CREATE TABLE movie_actors (
  id serial primary key,
  movie_id INTEGER,
  actor_id INTEGER
);

CREATE TABLE movie_directors (
  id serial primary key,
  movie_id INTEGER,
  director_id INTEGER
);

CREATE TABLE directors (
  id serial,
  name TEXT
);
