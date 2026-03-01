import unittest
from src.inventory_engine import reconcile_inventory


class InventoryCalculationTests(unittest.TestCase):

    def test_inventory_reduction(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 20,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 5}
        result = reconcile_inventory(inventory, sales)
        self.assertEqual(result[0]["final_stock"], 15)

    def test_inventory_not_negative(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 5,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 10}
        result = reconcile_inventory(inventory, sales)
        self.assertEqual(result[0]["final_stock"], 0)

    def test_zero_stock_status(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 5,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 5}
        result = reconcile_inventory(inventory, sales)
        self.assertEqual(result[0]["stock_status"], "OUT_OF_STOCK")


class StockStatusTests(unittest.TestCase):

    def test_available_status(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 20,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 5}
        result = reconcile_inventory(inventory, sales)
        self.assertEqual(result[0]["stock_status"], "AVAILABLE")

    def test_low_stock_status(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 10,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 5}
        result = reconcile_inventory(inventory, sales)
        self.assertEqual(result[0]["stock_status"], "LOW_STOCK")

    def test_out_of_stock_status(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 5,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 5}
        result = reconcile_inventory(inventory, sales)
        self.assertEqual(result[0]["stock_status"], "OUT_OF_STOCK")


class AdvancedMetricsTests(unittest.TestCase):

    def test_stock_utilization_percentage(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 20,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 5}
        result = reconcile_inventory(inventory, sales)

        # 5 sold out of 20 = 25%
        self.assertEqual(result[0]["stock_utilization_percentage"], 25.0)

    def test_estimated_days_until_stockout(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 30,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {"1": 30}  # 30 sold in 30 days

        result = reconcile_inventory(inventory, sales)

        # final stock = 0 → 0 days
        self.assertEqual(result[0]["estimated_days_until_stockout"], 0)

    def test_no_sales_estimation_none(self):
        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 30,
                "unit_price": 10,
                "category": "X"
            }
        }
        sales = {}

        result = reconcile_inventory(inventory, sales)

        self.assertIsNone(result[0]["estimated_days_until_stockout"])