#!/usr/bin/python3
"""Test City for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock
City = models.city.City
module_doc = models.city.__doc__


class TestCityDocs(unittest.TestCase):
    """Tests to check the documentation and style of City class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.city_funcs = inspect.getmembers(City, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/city.py conforms to PEP8."""
        for path in ['models/city.py', 'tests/test_models/test_city.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None, "city.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "city.py needs a docstring")

    def test_class_docstring(self):
        """Test for the City class docstring"""
        self.assertIsNot(City.__doc__, None, "City class needs a docstring")
        self.assertTrue(len(City.__doc__) >= 1, "City class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in City methods"""
        for func in self.city_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestCity(unittest.TestCase):
    """Test the City class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = City()
        self.assertIs(type(inst), City)
        inst.name = "New York"
        inst.state_id = "NY"
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "state_id": str
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "New York")
        self.assertEqual(inst.state_id, "NY")

    def test_datetime_attributes(self):
        """Test that two City instances have different datetime objects
        and that upon creation have identical updated_at and created_at value."""
        tic = datetime.now()
        inst1 = City()
        toc = datetime.now()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        inst2 = City()
        toc = datetime.now()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = City()
        inst2 = City()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid, '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_city = City()
        my_city.name = "New York"
        my_city.state_id = "NY"
        d = my_city.to_dict()
        expected_attrs = ["id", "created_at", "updated_at", "name", "state_id", "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'City')
        self.assertEqual(d['name'], "New York")
        self.assertEqual(d['state_id'], "NY")

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        city = City()
        new_d = city.to_dict()
        self.assertEqual(new_d["__class__"], "City")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], city.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], city.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        city = City()
        string = "[City] ({}) {}".format(city.id, city.__dict__)
        self.assertEqual(string, str(city))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls `storage.save`"""
        city = City()
        old_created_at = city.created_at
        old_updated_at = city.updated_at
        city.save()
        new_created_at = city.created_at
        new_updated_at = city.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
