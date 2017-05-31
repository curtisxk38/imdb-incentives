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
        positive = [", VA", "Virginia, USA", "Virginia Beach", ", Virginia", "University of Virginia", "Supreme Court of Virginia"]
        negative = ["West Virginia"]

        # if any value to be avoided is in the location string, then return false
        # the occurence of a negative string takes precedence over the occurence of a positive string
        for neg in negative:
            if neg in location:
                return False

        # after that, if a positive value is found return true
        for pos in positive:
            if pos in location:
                return True

        # after that, no positive or negative values were found, so just return false
        return False

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