import sqlite3
import io

import constants


class LocationReader():
    def __init__(self, conn, only_virginia=True):
        self.media = set()
        self.conn = conn
        self.c = self.conn.cursor()
        self.only_virginia = only_virginia

    def main(self):
        with io.open("locations.list", encoding="latin-1") as list_file:
            for line in list_file:
                self.process(line)

    def process(self, line):
        tab_delimited = line.split("\t") # split line at tab characters
        title = tab_delimited[0] # title is always the first string before tabs
        location = tab_delimited[-1] # location is always the last string after all the tab characters

        state_index = self.search_loc(location)

        # If the location is in the USA, then process it further and save it to the database
        if state_index != -1:
            self.save_to_db(title, location, state_index)

    def search_loc(self, location):
        usa_token = ", USA"
        
        if self.only_virginia:
            va = "Virginia"
            wva = "West Virginia"
            if va + usa_token in location and wva + usa_token not in location:
                return constants.states.index(va)
            else:
                return -1
        
        else:
            for index, state in enumerate(constants.states):
                if state + usa_token in location:
                    return index

            # No state was found for this location string
            return -1

    def save_to_db(self, title, location, state_index):
        if title not in self.media:
            self.media.add(title)
            media_type, year = self.parse_title(title)
            self.c.execute('''INSERT INTO media(name, media_type, year) VALUES (?, ?, ?)''', (title, media_type, year))
        
        try:
            self.c.execute('''INSERT INTO locations VALUES (?, ?, ?)''', (title, location, state_index))
        except sqlite3.IntegrityError:
            print("<{}> at <{}> is a duplicate, ignoring".format(title, location))
        
        self.conn.commit()

    def parse_title(self, title):
        """Parse title string for type and year
        See https://contribute.imdb.com/updates/guide/title_formats for explanation"""
        media_type = 1 # default assumption to Film

        open_p, close_p, year = self.find_year_token(title)

        # year is gauranteed to be a digit if not None by find_year_token()
        if year is not None:
            year = int(year) 
        
        # if find_year_token couldn't find the year token, the we can't find the media_type either
        if open_p is None and close_p is None:
            return None, year
        
        metadata = title[close_p + 2:] # the characters after the space after the close paranthese

        if metadata == "(TV)":
            media_type = 2
        elif metadata == "(V)":
            media_type = 3
        elif title[0] == '"':
            # could be TV series or TV episode
            if metadata.startswith("{"): # start of the episode name
                media_type = 5
            else:
                media_type = 4

        return media_type, year

    def find_year_token(self, title):
        """Given a title string find the part that has (yyyy) in it
            This is needed for further processing of the title string
        """
        potential_year = ""
        end = len(title)

        # find the last occurences of parentheses before the end variable
        # check if the characters between are a digit, if they aren't
        # then check for the next to last occurences of parentheses
        # We have to start at the back because the actual media title,
        #  could have a well formed year token in it (by that I mean inside the parentheses there could be a 4 digit integer)
        # This seems to cover all edge cases that occur in the IMDb data
        while not potential_year.isdigit():
            last_open_p = title.rfind("(", 0, end)
            last_close_p = title.rfind(")", 0, end)

            if last_open_p == -1 or last_close_p == -1:
                print("Malformed year token in <{}>, unable to process this title".format(title))
                return None, None, None

            potential_year = title[last_open_p+1:last_open_p+5]

            # Some of the data in the imdb is well formed, just the year is unknown
            # so we still want to return the parentheses locations so that the media type can be found
            if potential_year == "????":
                print("Unknown year for <{}>".format(title))
                return last_open_p, last_close_p, None
            
            # update which index of title string we have checked already for the year token
            end = last_open_p

        return last_open_p, last_close_p, potential_year



if __name__ == "__main__":
    conn = sqlite3.connect("imdb.db")
    l = LocationReader(conn)
    l.main()
    conn.close()