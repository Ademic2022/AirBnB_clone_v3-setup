import unittest
import models
from models.engine.db_storage import DBStorage
from models.state import State


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        # Connect to the test database
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        # Close the session and disconnect from the test database
        self.db.close()

    def test_all_method_returns_dictionary(self):
        # Test if the all method returns a dictionary
        result = self.db.all()
        self.assertIsInstance(result, dict)

    def test_all_method_returns_dictionary_for_state(self):
        # Test if the all method returns a dictionary with State objects
        result = self.db.all(State)
        for key, value in result.items():
            self.assertIsInstance(value, State)

    def test_new_method_adds_to_session(self):
        # Test if the new method adds an object to the session
        state = State(name="New York")
        self.db.new(state)
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertIn(key, self.db._DBStorage__session.new)

    def test_save_method_saves_changes(self):
        # Test if the save method saves changes to the database
        state = State(name="California")
        self.db.new(state)
        self.db.save()
        self.assertIn(state, self.db._DBStorage__session)

    def test_delete_method_deletes_from_session(self):
        # Test if the delete method deletes an object from the session
        state = State(name="Florida")
        self.db.new(state)
        self.db.save()
        self.db.delete(state)
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertNotIn(key, self.db._DBStorage__session)

    def test_get_method_returns_object_by_id(self):
        # Test if the get method retrieves an object by its class and id
        state = State(name="Texas")
        self.db.new(state)
        self.db.save()
        retrieved_state = self.db.get("State", state.id)
        self.assertEqual(state, retrieved_state)

    def test_count_method_counts_objects(self):
        # Test if the count method returns the correct count of objects
        count = self.db.count()
        self.assertEqual(count, len(models.storage.all()))

    def test_count_method_counts_objects_of_specified_class(self):
        # Test if the count method returns the correct count of objects
        # of a specified class
        count = self.db.count("State")
        self.assertEqual(count, len(models.storage.all("State")))


if __name__ == "__main__":
    unittest.main()
