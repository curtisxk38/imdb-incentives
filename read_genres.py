import sqlite3
import io

import utilities


class GenreReader():
    def __init__(self, conn):
        self.conn = conn
        self.c = self.conn.cursor()
        self.last_title = ""
        self.media = utilities.load_media(self.c)

    def main(self):
        with io.open("genres.list", encoding="utf-8", errors="ignore") as list_file:
            for line in list_file:
                self.process(line)
                if len(self.media) == 0:
                    break

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