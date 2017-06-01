import sqlite3
import os
import sys

from read_locations import LocationReader
from read_genres import GenreReader
from read_business import BusinessReader

def create_db(conn):
    c = conn.cursor()
    # Create tables
    c.execute('''CREATE TABLE media
                 (name text PRIMARY KEY,
                  media_type integer,
                  budget real,
                  gross real,
                  year integer
                  )''')
    c.execute('''CREATE TABLE locations
                 (
                 name text,
                 location text,
                 state_index integer,
                 PRIMARY KEY (name, location),
                 FOREIGN KEY(name) REFERENCES media(name)
                 )''')
    c.execute('''CREATE TABLE genres
                 (name text,
                  genre text,
                  PRIMARY KEY (name, genre)
                  FOREIGN KEY(name) REFERENCES media(name)
                  )''')
    # save
    conn.commit()

def main():
    conn = None

    if not os.path.isfile("imdb.db"):
        conn = sqlite3.connect("imdb.db")
        create_db(conn)
    else:
        conn = sqlite3.connect("imdb.db")

    if len(sys.argv) >= 2 and sys.argv[1] == "all":
      print("Finding media filmed in the USA")
      LocationReader(conn, only_virginia=False).main()
    else:
      print("Finding media filmed in Virginia...")
      LocationReader(conn).main()
    print("Adding genres to found media...")
    GenreReader(conn).main()
    print("Adding business information to found media...")
    BusinessReader(conn).main()

    conn.close()

if __name__ == "__main__":
    main()