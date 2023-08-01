import unittest
from models.engine.db_storage import DBStorage
from models.state import State


class TestDBStorage(unittest.TestCase):
    def setUp(self):
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        self.db.close()

    def test_all_method_returns_dictionary(self):
        result = self.db.all()
        self.assertIsInstance(result, dict)

    def test_all_method_returns_dictionary_for_state(self):
        result = self.db.all(State)
        for key, value in result.items():
            self.assertIsInstance(value, State)

    def test_new_method_adds_to_session(self):
        state = State(name="New York")
        self.db.new(state)
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertIn(key, self.db._DBStorage__session.new)

    def test_save_method_saves_changes(self):
        state = State(name="California")
        self.db.new(state)
        self.db.save()
        self.assertIn(state, self.db._DBStorage__session)

    def test_delete_method_deletes_from_session(self):
        state = State(name="Florida")
        self.db.new(state)
        self.db.save()
        self.db.delete(state)
        key = "{}.{}".format(type(state).__name__, state.id)
        self.assertNotIn(key, self.db._DBStorage__session)

    def test_get_method_returns_object_by_id(self):
        state = State(name="Texas")
        self.db.new(state)
        self.db.save()
        retrieved_state = self.db.get("State", state.id)
        self.assertEqual(state, retrieved_state)

    def test_count_method_counts_objects(self):
        count = self.db.count()
        self.assertEqual(count, len(self.db.all()))

    def test_count_method_counts_objects_of_specified_class(self):
        count = self.db.count("State")
        self.assertEqual(count, len(self.db.all("State")))


if __name__ == "__main__":
    unittest.main()
