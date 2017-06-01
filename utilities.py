import sqlite3

def load_media(cursor):
    # Get all media names from media and put them in a set
    query = cursor.execute('''SELECT name FROM media''').fetchall()
    flatten = [name for result in query for name in result]
    return set(flatten)