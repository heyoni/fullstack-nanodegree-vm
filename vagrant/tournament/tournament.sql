-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
-- DROP TABLE IF EXISTS games;
-- DROP TABLE IF EXISTS players;
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
  id   SERIAL,
  name TEXT,
  PRIMARY KEY (id)
);
CREATE TABLE games (
  id SERIAL,
  winner INT,
  loser  INT,
  PRIMARY KEY (id),
  FOREIGN KEY (winner) REFERENCES players (id),
  FOREIGN KEY (loser) REFERENCES players (id)
);

INSERT INTO players (name) VALUES
  ('jonathan revah'),
  ('lauren witter');

CREATE VIEW standing AS
  SELECT
    players.id,
    players.name,
    count(games.winner)                               AS wins,
    (SELECT count(*)
     FROM games
     WHERE loser = players.id OR winner = players.id) AS matches
  FROM players
    LEFT JOIN games ON games.winner = players.id
  GROUP BY players.id
  ORDER BY wins
  DESC;