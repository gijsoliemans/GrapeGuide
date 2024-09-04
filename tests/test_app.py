# tests/test_app.py

import unittest
from app import app
from data.data import wines
class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config.TestConfig')
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to GrapeGuide!', response.data)

    def test_about_page(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About GrapeGuide', response.data)

    def test_search_page(self):
        response = self.app.get('/search')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Wines', response.data)

    def test_wines_page(self):
        response = self.app.get('/wines')
        self.assertEqual(response.status_code, 200)
        for wine in wines:
            wine_name_encoded = wine['name'].replace("'", "&#39;").encode()
            self.assertIn(wine_name_encoded, response.data)


if __name__ == "__main__":
    unittest.main()