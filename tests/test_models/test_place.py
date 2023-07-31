#!/usr/bin/python3
"""Test Place for expected behavior and documentation"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
import time
import unittest
from unittest import mock
Place = models.place.Place
module_doc = models.place.__doc__


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.place_funcs = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/place.py conforms to PEP8."""
        for path in ['models/place.py', 'tests/test_models/test_place.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None, "place.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "place.py needs a docstring")

    def test_class_docstring(self):
        """Test for the Place class docstring"""
        self.assertIsNot(Place.__doc__, None, "Place class needs a docstring")
        self.assertTrue(len(Place.__doc__) >= 1, "Place class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func in self.place_funcs:
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


class TestPlace(unittest.TestCase):
    """Test the Place class"""
    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = Place()
        self.assertIs(type(inst), Place)
        inst.name = "Cozy Cabin"
        inst.city_id = "NYC"
        inst.user_id = "user123"
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "city_id": str,
            "user_id": str,
            "description": str,
            "number_rooms": int,
            "number_bathrooms": int,
            "max_guest": int,
            "price_by_night": int,
            "latitude": float,
            "longitude": float,
            "amenity_ids": list
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Cozy Cabin")
        self.assertEqual(inst.city_id, "NYC")
        self.assertEqual(inst.user_id, "user123")

    def test_datetime_attributes(self):
        """Test that two Place instances have different datetime objects
        and that upon creation have identical updated_at and created_at value."""
        tic = datetime.now()
        inst1 = Place()
        toc = datetime.now()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now()
        inst2 = Place()
        toc = datetime.now()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = Place()
        inst2 = Place()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid, '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_place = Place()
        my_place.name = "Cozy Cabin"
        my_place.city_id = "NYC"
        my_place.user_id = "user123"
        d = my_place.to_dict()
        expected_attrs = ["id", "created_at", "updated_at", "name", "city_id", "user_id", "description",
                          "number_rooms", "number_bathrooms", "max_guest", "price_by_night",
                          "latitude", "longitude", "amenity_ids", "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'Place')
        self.assertEqual(d['name'], "Cozy Cabin")
        self.assertEqual(d['city_id'], "NYC")
        self.assertEqual(d['user_id'], "user123")

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        place = Place()
        new_d = place.to_dict()
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], place.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], place.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))

    @mock.patch('models.storage')
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls `storage.save`"""
        place = Place()
        old_created_at = place.created_at
        old_updated_at = place.updated_at
        place.save()
        new_created_at = place.created_at
        new_updated_at = place.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
