#!/usr/bin/python3
"""
Contains the TestDBStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models import db_storage
from models.base_model import BaseModel
import pep8
import unittest
DBStorage = db_storage.DBStorage


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbstorage_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_db_storage_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbstorage_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    def test_all(self):
        """Test all method"""
        storage = DBStorage()
        all_objs = storage.all()
        self.assertIsNotNone(all_objs)
        self.assertEqual(type(all_objs), dict)

    def test_new(self):
        """Test new method"""
        storage = DBStorage()
        new_obj = BaseModel()
        storage.new(new_obj)
        key = "{}.{}".format(type(new_obj).__name__, new_obj.id)
        all_objs = storage.all()
        self.assertIsNotNone(all_objs[key])

    def test_save(self):
        """Test save method"""
        storage = DBStorage()
        new_obj = BaseModel()
        storage.new(new_obj)
        storage.save()
        key = "{}.{}".format(type(new_obj).__name__, new_obj.id)
        all_objs = storage.all()
        self.assertIsNotNone(all_objs[key])

    def test_delete(self):
        """Test delete method"""
        storage = DBStorage()
        new_obj = BaseModel()
        storage.new(new_obj)
        key = "{}.{}".format(type(new_obj).__name__, new_obj.id)
        all_objs = storage.all()
        self.assertIsNotNone(all_objs[key])
        storage.delete(new_obj)
        all_objs = storage.all()
        self.assertNotIn(key, all_objs)

    def test_reload(self):
        """Test reload method"""
        storage = DBStorage()
        storage.reload()
        self.assertIsNotNone(DBStorage._DBStorage__session)

    def test_get(self):
        """Test get method"""
        storage = DBStorage()
        new_obj = BaseModel()
        key = "{}.{}".format(type(new_obj).__name__, new_obj.id)
        all_objs = storage.all()
        self.assertIsNotNone(all_objs[key])
        obj = storage.get("BaseModel", new_obj.id)
        self.assertIsNotNone(obj)
        self.assertEqual(obj, all_objs[key])

    def test_count(self):
        """Test count method"""
        storage = DBStorage()
        all_objs = storage.all()
        count_all_objs = len(all_objs)
        count_obj = storage.count()
        self.assertEqual(count_all_objs, count_obj)

    def test_count_cls(self):
        """Test count method with class as argument"""
        storage = DBStorage()
        all_objs = storage.all()
        count_base = len(all_objs["BaseModel"])
        count_base_cls = storage.count("BaseModel")
        self.assertEqual(count_base, count_base_cls)


if __name__ == '__main__':
    unittest.main()
