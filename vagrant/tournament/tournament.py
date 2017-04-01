#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname=tournament")
        cur = conn.cursor()
        return conn, cur
    except:
        print("Error establishing a connection to database.")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    c.execute('TRUNCATE games')
    conn.commit()
    c.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    # Benefits of using TRUNCATE over DELETE
    # https://www.postgresql.org/docs/9.1/static/sql-truncate.html
    c.execute('TRUNCATE players CASCADE')
    conn.commit()
    c.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
    c.execute("SELECT count(*) FROM players")
    return int(c.fetchone()[0])


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, c = connect()
    query = 'INSERT INTO players (name) VALUES (%s)'
    params = (name,)
    c.execute(query, params)
    conn.commit()
    c.close()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = connect()
    c.execute("SELECT * FROM standing")
    results = c.fetchall()
    c.close()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = connect()
    query = "INSERT INTO games (winner, loser) VALUES (%s, %s)"
    params = (winner, loser)
    c.execute(query, params)
    conn.commit()
    c.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn, c = connect()
    # c.execute("SELECT id, name FROM standing")
    standings = playerStandings()
    counter = 0
    pairs = []
    while counter < len(standings):
        pairs.append((standings[counter][0], standings[counter][1],
                      standings[counter + 1][0], standings[counter + 1][1]))
        counter += 2
    conn.commit()
    c.close()
    conn.close()
    return pairs


if __name__ == '__main__':
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")
    standings = playerStandings()
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
