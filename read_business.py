import sqlite3
import io

import utilities


class BusinessReader():
    def __init__(self, conn):
        self.conn = conn
        self.c = self.conn.cursor()
        # entry of business information about a particular movie
        self.entry = []
        self.media = utilities.load_media(self.c)

    def main(self):
        processing = False
        with io.open("business.list", encoding="utf-8", errors="ignore") as list_file:
            for line in list_file:
                if not processing and line == "BUSINESS LIST\n":
                    processing = True
                if processing:
                    self.process(line)

    def process(self, line):
        if line == "-------------------------------------------------------------------------------\n":
            self.process_entry()
            self.entry = [] 
        else:
            self.entry.append(line)

    def process_entry(self):
        movie_token = "MV: "
        budget_token = "BT: "
        gross_token = "GR: "

        movie = budget = gross = None

        for line in self.entry:
            if line.startswith(movie_token):
                movie = line[len(movie_token):].strip()
            if line.startswith(budget_token):
                budget = line[len(budget_token):].strip()
            if line.startswith(gross_token):
                gross = line[len(gross_token):].strip()
                # After you find the first gross token stop reading because the ones after that are for earlier dates
                break

        if movie in self.media and (budget is not None or gross is not None):
            self.media.remove(movie)
            self.save_to_db(movie, budget, gross)

    def convert_money(self, money_string):
        money_string = money_string.split(" ")[1].strip()
        return float(money_string.replace(",", ""))

    def save_to_db(self, title, budget, gross):
        budget = self.convert_money(budget) if budget is not None else None
        gross = self.convert_money(gross) if gross is not None else None

        self.c.execute('''UPDATE media SET budget = ?, gross = ? WHERE name = ?''', (budget, gross, title))
        self.conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect("imdb.db")
    b = BusinessReader(conn)
    b.main()
    conn.close()