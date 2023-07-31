#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

import inspect
import models
from models import file_storage
from models.base_model import BaseModel
import pep8
import unittest
FileStorage = file_storage.FileStorage


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.filestorage_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_file_storage_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.filestorage_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_all(self):
        """Test all method"""
        storage = FileStorage()
        all_objs = storage.all()
        self.assertIsNotNone(all_objs)
        self.assertEqual(type(all_objs), dict)

    def test_new(self):
        """Test new method"""
        storage = FileStorage()
        new_obj = BaseModel()
        storage.new(new_obj)
        key = "{}.{}".format(type(new_obj).__name__, new_obj.id)
        all_objs = storage.all()
        self.assertIsNotNone(all_objs[key])

    def test_save(self):
        """Test save method"""
        storage = FileStorage()
        new_obj = BaseModel()
        storage.new(new_obj)
        storage.save()
        key = "{}.{}".format(type(new_obj).__name__, new_obj.id)
        all_objs = storage.all()
        self.assertIsNotNone(all_objs[key])

    def test_delete(self):
        """Test delete method"""
        storage = FileStorage()
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
        storage = FileStorage()
        storage.reload()
        self.assertIsNotNone(FileStorage._FileStorage__objects)

    def test_close(self):
        """Test close method"""
        storage = FileStorage()
        storage.close()
        all_objs = storage.all()
        self.assertIsNotNone(all_objs)


if __name__ == '__main__':
    unittest.main()
