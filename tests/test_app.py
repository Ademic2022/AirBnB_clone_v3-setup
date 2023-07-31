#!/usr/bin/python3
""" Unittest for API routes """
import unittest
from api.v1.app import app


class TestAppRoutes(unittest.TestCase):
    """ Test class for API routes """

    def setUp(self):
        """ Set up the app for testing """
        self.client = app.test_client()

    def test_status_route(self):
        """ Test /status route """
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_stats_route(self):
        """ Test /stats route """
        response = self.client.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), dict)
        self.assertGreaterEqual(len(response.get_json()), 6)  # Check if all counts are present


if __name__ == "__main__":
    unittest.main()
