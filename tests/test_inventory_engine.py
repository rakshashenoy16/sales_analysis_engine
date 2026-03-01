import unittest
from src.inventory_engine import reconcile_inventory


class InventoryCalculationTests(unittest.TestCase):
    """
    Tests basic inventory reconciliation logic:
    - Stock reduction
    - Non-negative stock enforcement
    - Stock status determination
    """

    def test_inventory_reduction(self):
        """Stock should reduce correctly when valid sales occur."""

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

        # 20 - 5 = 15
        self.assertEqual(result[0]["final_stock"], 15)

    def test_inventory_not_negative(self):
        """Final stock should never go below zero."""

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

        # Should be capped at 0
        self.assertEqual(result[0]["final_stock"], 0)

    def test_zero_stock_status(self):
        """Stock status should be OUT_OF_STOCK when final stock is zero."""

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
    """
    Tests stock status classification:
    - AVAILABLE
    - LOW_STOCK
    - OUT_OF_STOCK
    """

    def test_available_status(self):
        """Stock > 10 should be marked as AVAILABLE."""

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
        """Stock between 1 and 10 should be marked as LOW_STOCK."""

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
        """Stock reaching zero should be OUT_OF_STOCK."""

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
    """
    Tests advanced analytics metrics:
    - Stock utilization percentage
    - Estimated days until stockout
    """

    def test_stock_utilization_percentage(self):
        """Should calculate correct utilization percentage."""

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
        """If final stock is zero, estimated days should be 0."""

        inventory = {
            "1": {
                "product_name": "A",
                "current_stock": 30,
                "unit_price": 10,
                "category": "X"
            }
        }

        # Simulating full stock sold
        sales = {"1": 30}

        result = reconcile_inventory(inventory, sales)

        self.assertEqual(result[0]["estimated_days_until_stockout"], 0)

    def test_no_sales_estimation_none(self):
        """If no sales exist, stockout estimation should be None."""

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