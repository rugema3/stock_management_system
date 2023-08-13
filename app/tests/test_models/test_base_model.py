#!/usr/bin/env python
"""Test base_model.

This module tests the base_model to make sure everything is robust
and is fully tested.
"""
import unittest
from app.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test BaseModel class."""

    def test_class_present(self):
        """Test if the BaseModel class is present."""
        a = BaseModel()
        self.assertIsInstance(a, BaseModel)  # Is 'a' an instance of BaseModel

    def test_attributes_present(self):
        """Test if the attributes are available."""
        a = BaseModel()
        self.assertIsNotNone(a.item_id)  # check if 'item_id' is present
        self.assertIsNotNone(a.item_name)  # Check if 'item_name' is present
        self.assertIsNotNone(a.quantity)  # check if 'quantity' is present
        self.assertIsNotNone(a.price)  # Check if 'price' is present
        self.assertIsNotNone(a.category)  # Check if 'Category' is present

    def test_if_id_is_str(self):
        """Test if the generated item_id is a string."""
        a = BaseModel()
        self.assertIsInstance(a.item_id, str)

    def test_if_name_is_str(self):
        """Test if item_name is a string."""
        a = BaseModel()
        self.assertIsInstance(a.item_name, str)

    def test_if_quantity_is_int(self):
        """Test if quantity is an integer."""
        a = BaseModel()
        self.assertIsInstance(a.quantity, int)

    def test_if_price_is_float(self):
        """Test if price is a float."""
        a = BaseModel()
        self.assertIsInstance(a.price, float)

    def test_item_name_not_str(self):
        """Test when item_name is not a string"""
        item_name = 3
        a = BaseModel()
        with self.assertRaises(TypeError):
            a


if __name__ == '__main__':
    unittest.main()

