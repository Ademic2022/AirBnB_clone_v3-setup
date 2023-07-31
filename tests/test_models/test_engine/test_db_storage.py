import unittest
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models import storage
from models.base_model import BaseModel
from os import getenv
from sqlalchemy import Column, String, Integer


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        """Method to set up the testing environment"""
        self.my_model = State()
        self.my_model.name = "California"
        self.my_model.save()

    def test_all_method(self):
        """Method to test the 'all' method of the DBStorage class"""
        # Test all() method without specifying a class argument
        all_objects = storage.all()
        self.assertEqual(len(all_objects), 1)

        # Test all() method with a class argument
        all_states = storage.all("State")
        self.assertEqual(len(all_states), 1)

        # Test all() method with an invalid class argument
        all_invalid = storage.all("Invalid")
        self.assertEqual(len(all_invalid), 0)

    def test_new_and_save_methods(self):
        """Method to test the 'new' and 'save' methods of the DBStorage class"""
        # Test 'new' method
        new_state = State()
        new_state.name = "New York"
        storage.new(new_state)

        # Test 'save' method
        self.assertTrue(hasattr(new_state, "id"))
        new_state.save()

        all_objects = storage.all()
        self.assertEqual(len(all_objects), 2)

    def test_delete_method(self):
        """Method to test the 'delete' method of the DBStorage class"""
        # Test delete() method with an existing object
        all_objects = storage.all()
        self.assertEqual(len(all_objects), 1)
        state_id = list(all_objects.keys())[0]
        state = all_objects[state_id]
        storage.delete(state)
        all_objects = storage.all()
        self.assertEqual(len(all_objects), 0)

        # Test delete() method with a non-existing object
        state = State()
        storage.delete(state)
        all_objects = storage.all()
        self.assertEqual(len(all_objects), 0)

    def test_reload_and_close_methods(self):
        """Method to test the 'reload' and 'close' methods of the DBStorage class"""
        # Test reload() and close() methods
        storage.reload()
        all_objects = storage.all()
        self.assertEqual(len(all_objects), 1)
        storage.close()

    def test_get_method(self):
        """Method to test the 'get' method of the DBStorage class"""
        # Test get() method with an existing object
        all_objects = storage.all()
        state_id = list(all_objects.keys())[0]
        state = storage.get("State", state_id)
        self.assertEqual(state.name, "California")

        # Test get() method with a non-existing object
        state = storage.get("State", "invalid_id")
        self.assertIsNone(state)

    def test_count_method(self):
        """Method to test the 'count' method of the DBStorage class"""
        # Test count() method without specifying a class argument
        count_all = storage.count()
        self.assertEqual(count_all, 1)

        # Test count() method with a class argument
        count_states = storage.count("State")
        self.assertEqual(count_states, 1)

        # Test count() method with an invalid class argument
        count_invalid = storage.count("Invalid")
        self.assertEqual(count_invalid, 0)


if __name__ == "__main__":
    unittest.main()

# #!/usr/bin/python3
# """ Test module for the Database storage"""

# import unittest
# import pycodestyle
# from models.engine.db_storage import DBStorage


# class TestDBStorage(unittest.TestCase):
#     """ Clas TestDBStorage for testing the database storage"""
    
#     def testPycodeStyle(self):
#         """Test for pycodestyle compliancy in DBStorage"""
#         style = pycodestyle.StyleGuide(quiet=True)
#         p = style.check_files(['models/engine/db_storage.py'])
#         self.assertEqual(p.total_errors, 0, "fix pep8")

#     def test_docstring_DBStorage(self):
#         """Test for docstring in DBStorage"""
#         self.assertIsNotNone(DBStorage.__doc__)
#         self.assertIsNotNone(DBStorage.__init__.__doc__)
#         self.assertIsNotNone(DBStorage.all.__doc__)
#         self.assertIsNotNone(DBStorage.new.__doc__)
#         self.assertIsNotNone(DBStorage.save.__doc__)
#         self.assertIsNotNone(DBStorage.delete.__doc__)
#         self.assertIsNotNone(DBStorage.reload.__doc__)


# if __name__ == "__main__":
#     unittest.main()
