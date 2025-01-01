#!/usr/bin/python3
"""Module for testing file storage."""
import os
import unittest
from models import storage
from models.base_model import BaseModel


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test")
class test_fileStorage(unittest.TestCase):
    """Test cases for FileStorage class."""

    def setUp(self):
        """Remove storage file at start of tests."""
        del_list = []
        for key in storage._FileStorage__objects.keys():
            del_list.append(key)
        for key in del_list:
            del storage._FileStorage__objects[key]

    def tearDown(self):
        """Remove storage file at end of tests."""
        try:
            os.remove("file.json")
        except Exception:
            pass

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_obj_list_empty(self):
        """Tests that __objects is empty at start of tests."""
        self.assertEqual(len(storage.all()), 0)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_new(self):
        """Tests that new objects are properly added to __objects."""
        temp = BaseModel()
        for obj in storage.all().values():
            temp = obj
            self.assertTrue(temp is obj)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_all(self):
        """Tests that all() returns __objects."""
        new = BaseModel()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_base_model_instantiation(self):
        """Tests that a new instance of BaseModel is created."""
        new = BaseModel()
        self.assertFalse(os.path.exists("file.json"))

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_empty(self):
        """Tests all() returns an empty dictionary if __objects is empty."""
        new = BaseModel()
        thing = new.to_dict()
        new.save()
        new2 = BaseModel(**thing)
        self.assertNotEqual(os.path.getsize("file.json"), 0)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_save(self):
        """Tests that save() properly saves objects to file.json."""
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists("file.json"))

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_reload(self):
        """Tests that reload() properly loads objects from file.json."""
        new = BaseModel()
        storage.save()
        storage.reload()
        for obj in storage.all().values():
            self.assertEqual(new.to_dict()["id"], obj.to_dict()["id"])

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_reload_empty(self):
        """Tests that reload() properly loads an empty file.json."""
        with open("file.json", "w") as f:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_reload_from_nonexistent(self):
        """Tests that reload() properly loads from a nonexistent file.json."""
        self.assertEqual(storage.reload(), None)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_base_model_save(self):
        """Tests that save() properly saves BaseModel objects to file.json."""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists("file.json"))

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_type_path(self):
        """Tests that __file_path is a string."""
        self.assertEqual(type(storage._FileStorage__file_path), str)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_type_objects(self):
        """Tests that __objects is a dictionary."""
        self.assertEqual(type(storage.all()), dict)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_key_format(self):
        """Tests that the key for each object in __objects."""
        new = BaseModel()
        new.save()
        _id = new.to_dict()["id"]
        for key in storage.all().keys():
            temp = key
        self.assertEqual(temp, "BaseModel" + "." + _id)

    @unittest.skipIf(
        os.getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage test"
    )
    def test_storage_var_created(self):
        """Tests that a new instance of FileStorage is created."""
        from models.engine.file_storage import FileStorage

        self.assertEqual(type(storage), FileStorage)
