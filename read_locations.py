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
            media_type, year = self.parse_title(title)
            self.c.execute('''INSERT INTO media(name, media_type, year) VALUES (?, ?, ?)''', (title, media_type, year))
        
        try:
            self.c.execute('''INSERT INTO locations VALUES (?, ?)''', (title, location))
        except sqlite3.IntegrityError:
            print("{}: {} is a duplicate, ignoring".format(title, location))
        
        self.conn.commit()

    def parse_title(self, title):
        """Parse title string for type and year
        See https://contribute.imdb.com/updates/guide/title_formats for explanation"""
        media_type = 1 # default to Film
        year = None
        # find the opening parantheses that corresponds to the year in the title string
        open_p = title.find('(')
        close_p = title.find(')')
        if open_p == -1:
            raise ValueError("Can't find year (enclosed in parantheses) in {}".format(title))
        
        # separate the title string into parts: just the actual title an then the metadata at the end
        title_string = title[:open_p - 1] # minus 1 so as not to include the space between the actual title and the year
        
        year = title[open_p + 1: open_p + 5] # grab the 4 digits between the parantheses
        try:
            year = int(year)
        except ValueError:
            print("Malformed year token in {}, unable to find year".format(title))
            year = None
        
        metadata = title[close_p + 2:] # the characters after the space after the close paranthese

        if metadata == "(TV)":
            media_type = 2
        elif metadata == "(V)":
            media_type = 3
        elif title_string[0] == '"':
            # could be TV series or TV episode
            if metadata.startswith("{"): # start of the episode name
                media_type = 5
            else:
                media_type = 4

        return media_type, year



if __name__ == "__main__":
    conn = sqlite3.connect("imdb.db")
    l = LocationReader(conn)
    l.main()
    conn.close()