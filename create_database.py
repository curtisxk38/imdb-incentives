import sqlite3

def create_db():
    conn = sqlite3.connect("imdb.db")
    c = conn.cursor()
    # Create tables
    c.execute('''CREATE TABLE media
                 (name text, media_type text, budget real, gross real, year integer)''')
    c.execute('''CREATE TABLE locations
                 (name text, location text)''')
    # save
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()