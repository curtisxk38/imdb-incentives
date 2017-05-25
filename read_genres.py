import sqlite3


class GenreReader():
    def __init__(self, conn):
        self.media = set()
        self.conn = conn
        self.c = self.conn.cursor()
        self.last_title = ""

    def main(self):
        self.load_media()
        with open("genres.list", encoding="latin-1") as list_file:
            for line in list_file:
                self.process(line)
                if len(self.media) == 0:
                    break

    def load_media(self):
        # Get all media names from media and put them in a set
        query = self.c.execute('''SELECT name FROM media''').fetchall()
        flatten = [name for result in query for name in result]
        self.media = self.media.union(flatten)

    def process(self, line):
        tab_delimited = line.split("\t") # split line at tab characters
        title = tab_delimited[0] # title is always the first string before tabs
        genre = tab_delimited[-1] # genre is always the last string after all the tab characters

        if title != self.last_title:
            try:
                self.media.remove(self.last_title)
            except KeyError:
                pass
            self.last_title = title

        if title in self.media:
            self.save_to_db(title, genre)

    def save_to_db(self, title, genre):
        self.c.execute('''INSERT INTO genres VALUES (?, ?)''', (title, genre))
        self.conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect("imdb.db")
    r = GenreReader(conn)
    r.main()
    conn.close()