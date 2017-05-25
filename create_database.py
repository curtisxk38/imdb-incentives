import sqlite3

def create_db():
    conn = sqlite3.connect("imdb.db")
    c = conn.cursor()
    # Create tables
    c.execute('''CREATE TABLE media
                 (name text PRIMARY KEY,
                  media_type text,
                  budget real,
                  gross real,
                  year integer
                  )''')
    c.execute('''CREATE TABLE locations
                 (
                 name text PRIMARY KEY,
                 location text,
                 FOREIGN KEY(name) REFERENCES media(name)
                 )''')
    c.execute('''CREATE TABLE genres
                 (name text PRIMARY KEY,
                  genre text,
                  FOREIGN KEY(name) REFERENCES media(name)
                  )''')
    # save
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()