import unittest
import read_locations
import sqlite3

class TestMediaType(unittest.TestCase):
    def setUp(self):
        self.movie = 'Lilith asdf (1964)'
        self.for_video = 'Lights Out (2008) (V)'
        self.for_tv = "Life's Other Side (2007) (TV)"
        self.tv_series = '"100 Greatest Discoveries" (2004)'
        self.tv_episode = '"A Haunting (a subtitle)" (2005) {The Dark Side (#3.10)}'
        self.malformed = "asdf adsf (????a) (TV)"
        self.paren_movie = "Flight Level Three Twenty Four (FL324) (2008) (TV)" # movie with parentheses in title

        self.conn = sqlite3.connect("imdb.db")

        self.lr = read_locations.LocationReader(self.conn)

    def test_movie(self):
        media_type, year = self.lr.parse_title(self.movie)
        self.assertEqual(year, 1964)
        self.assertEqual(media_type, 1)

    def test_for_video(self):
        media_type, year = self.lr.parse_title(self.for_video)
        self.assertEqual(year, 2008)
        self.assertEqual(media_type, 3)

    def test_for_tv(self):
        media_type, year = self.lr.parse_title(self.for_tv)
        self.assertEqual(year, 2007)
        self.assertEqual(media_type, 2)

    def test_for_tv_series(self):
        media_type, year = self.lr.parse_title(self.tv_series)
        self.assertEqual(year, 2004)
        self.assertEqual(media_type, 4)

    def test_for_tv_episode(self):
        media_type, year = self.lr.parse_title(self.tv_episode)
        self.assertEqual(year, 2005)
        self.assertEqual(media_type, 5)

    def test_malformed(self):
        media_type, year = self.lr.parse_title(self.malformed)
        self.assertIsNone(year)
        self.assertEqual(media_type, 2)

    def test_parse_year(self):
        openp, closep, year = self.lr.find_year_token(self.tv_episode)
        self.assertEqual(year, "2005")
        openp, closep, year = self.lr.find_year_token(self.paren_movie)
        self.assertEqual(year, "2008")
