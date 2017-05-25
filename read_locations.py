import sqlite3


class LocationReader():
    def __init__(self, conn):
        self.media = set()
        self.conn = conn
        self.c = self.conn.cursor()

    def main(self):
        line_limit = 100
        line_debug = 0
        with open("locations.list", encoding="latin-1") as list_file:
            for line in list_file:
                #line_debug += 1
                self.process(line)
                if line_debug > line_limit:
                    break

    def process(self, line):
        tab_delimited = line.split("\t") # split line at tab characters
        title = tab_delimited[0] # title is always the first string before tabs
        location = tab_delimited[-1] # location is always the last string after all the tab characters

        if self.search_loc(location):
            self.save_to_db(title, location)

    def search_loc(self, location):
        key1 = ", VA"
        key2 = "Virginia"
        return key1 in location or key2 in location

    def save_to_db(self, title, location):
        if title not in self.media:
            self.media.add(title)
            self.c.execute('''INSERT INTO media(name) VALUES (?)''', (title,))
        try:
            self.c.execute('''INSERT INTO locations VALUES (?, ?)''', (title, location))
        except sqlite3.IntegrityError:
            print("{}: {} is a duplicate, ignoring".format(title, location))
        self.conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect("imdb.db")
    l = LocationReader(conn)
    l.main()
    conn.close()