#!/usr/bin/python3
""" Test module for the Database storage"""

import unittest
import pycodestyle
from models.engine.db_storage import DBStorage
from models.state import State


class TestDBStorage(unittest.TestCase):
    """ Class TestDBStorage for testing the database storage"""

    def setUp(self):
        """ Set up the DBStorage instance for testing """
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """ Close the DBStorage session after each test """
        self.db.close()

    def testPycodeStyle(self):
        """ Test for pycodestyle compliancy in DBStorage """
        style = pycodestyle.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstring_DBStorage(self):
        """ Test for docstring in DBStorage """
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    def test_all_method_returns_dictionary(self):
        """ Test that all() method returns a dictionary """
        result = self.db.all()
        self.assertIsInstance(result, dict)

    def test_all_method_returns_dictionary_for_state(self):
        """ Test that all() method returns a dictionary of State objects """
        result = self.db.all(State)
        for key, value in result.items():
            self.assertIsInstance(value, State)

    # Add more test cases for other methods as needed...

if __name__ == "__main__":
    unittest.main()
