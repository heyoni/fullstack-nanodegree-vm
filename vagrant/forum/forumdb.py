#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #
    # posts.sort(key=lambda row: row['time'], reverse=True)
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute('SELECT * FROM posts ORDER BY time DESC')
    val = str(c.fetchone()[1])
    clean_val = (val)
    print(clean_val)
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in
             c.fetchall()]
    DB.close()
    return posts


## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    # t = time.strftime('%c', time.localtime())
    # this somehow sanitizes the input...
    c.execute("INSERT INTO posts (content) VALUES (%s)", (content,))
    # c.execute("INSERT INTO posts (content) VALUES ('%s')" % content)
    DB.commit()
    DB.close()
    # DB.append((t, content))


if __name__ == '__main__':
    print("we're in Maine!")
