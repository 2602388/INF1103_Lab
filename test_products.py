"""Checks every item in the Lab 7 testing list (section 7).
Run with:  python3 test_products.py   (or: python3 -m unittest -v test_products)"""
import contextlib
import io
import os
import tempfile
import unittest

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_manager import load_inventory, save_inventory
from physical_product import PhysicalProduct
from product import Product


def captured(func):
    """Runs func and returns everything it printed."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        func()
    return buffer.getvalue()


class TestProducts(unittest.TestCase):
    def setUp(self):
        self.guitar = PhysicalProduct("P001", "Guitar", 450.00, 5, 3.2)
        self.software = DigitalProduct("D001", "Operating System", 129.99, 100, 4500)

    def test_physical_stores_and_displays_weight(self):
        self.assertEqual(self.guitar.weight, 3.2)
        self.assertIn("3.20 kg", captured(self.guitar.display_information))

    def test_digital_stores_and_displays_download_size(self):
        self.assertEqual(self.software.download_size, 4500.0)
        self.assertIn("4500.00 MB", captured(self.software.display_information))

    def test_display_includes_parent_and_child_information(self):
        output = captured(self.guitar.display_information)
        self.assertIn("ID: P001", output)          # from Product
        self.assertIn("Weight:", output)           # from PhysicalProduct

    def test_both_subclasses_implement_get_fulfilment_info(self):
        self.assertIn("physical shipping", self.guitar.get_fulfilment_info())
        self.assertIn("digitally", self.software.get_fulfilment_info())

    def test_abstract_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("X001", "Generic", 10.0, 1)

    def test_interface_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_physical_products_calculate_shipping_cost(self):
        light = PhysicalProduct("P", "Light", 10, 1, 1)
        heavy = PhysicalProduct("P", "Heavy", 10, 1, 10)
        self.assertEqual(light.calculate_shipping_cost(), 7.00)
        self.assertEqual(heavy.calculate_shipping_cost(), 25.00)
        self.assertIsInstance(self.guitar, CanBeShipped)

    def test_digital_products_do_not_ship(self):
        self.assertNotIsInstance(self.software, CanBeShipped)
        self.assertFalse(hasattr(self.software, "calculate_shipping_cost"))

    def test_stock_rules_still_enforced(self):
        self.guitar.update_stock(20)
        self.assertEqual(self.guitar.stock, 20)
        with self.assertRaises(ValueError):
            self.guitar.update_stock(-1)


class TestInventory(unittest.TestCase):
    def test_inventory_operations_with_mixed_types(self):
        inventory = Inventory()
        self.assertTrue(inventory.add_product(PhysicalProduct("P001", "Guitar", 450, 5, 3.2)))
        self.assertTrue(inventory.add_product(DigitalProduct("D001", "OS", 129.99, 100, 4500)))
        self.assertFalse(inventory.add_product(DigitalProduct("D001", "Dup", 1, 1, 1)))
        self.assertEqual(inventory.search_product("D001").name, "OS")
        self.assertIsNone(inventory.search_product("NOPE"))
        inventory.search_product("P001").update_stock(9)
        self.assertEqual(inventory.search_product("P001").stock, 9)
        self.assertIn("Guitar", captured(inventory.display_all))


class TestPersistence(unittest.TestCase):
    def test_save_and_load_preserve_types_and_attributes(self):
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P001", "Guitar", 450, 5, 3.2))
        inventory.add_product(DigitalProduct("D001", "OS", 129.99, 100, 4500))

        path = os.path.join(tempfile.mkdtemp(), "inventory.json")
        save_inventory(inventory, path)
        restored = captured_load(path)

        guitar = restored.search_product("P001")
        software = restored.search_product("D001")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertIsInstance(software, DigitalProduct)
        self.assertEqual(guitar.weight, 3.2)
        self.assertEqual(software.download_size, 4500.0)
        self.assertEqual(software.stock, 100)

    def test_missing_file_starts_empty(self):
        restored = captured_load("definitely_not_here.json")
        self.assertEqual(restored.get_products(), [])

    def test_unknown_type_falls_back_to_empty(self):
        path = os.path.join(tempfile.mkdtemp(), "bad.json")
        with open(path, "w") as f:
            f.write('[{"type": "mystery", "id": "X", "name": "X", "price": 1, "stock": 1}]')
        self.assertEqual(captured_load(path).get_products(), [])


def captured_load(path):
    with contextlib.redirect_stdout(io.StringIO()):
        return load_inventory(path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
