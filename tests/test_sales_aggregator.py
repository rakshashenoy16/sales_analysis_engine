import unittest
from src.sales_aggregator import aggregate_sales


class SalesAggregationTests(unittest.TestCase):
    """
    Test suite for aggregate_sales function.

    Covers:
    - Valid aggregation logic
    - Date validation
    - Negative quantity handling
    - Unknown product handling
    - Data quality metrics tracking
    """

    def test_multiple_sales_aggregation(self):
        """Should correctly aggregate multiple valid transactions."""

        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "2024-04-10", "quantity_sold": "5"},
            {"product_id": "1", "transaction_date": "2024-04-15", "quantity_sold": "3"},
        ]

        # Execute aggregation
        result, processed, quality = aggregate_sales(sales, inventory)

        # Validate results
        self.assertEqual(result["1"], 8)  # 5 + 3
        self.assertEqual(processed, 2)    # Two valid transactions processed
        self.assertEqual(quality["valid_transactions"], 2)


    def test_invalid_transaction_date(self):
        """Should ignore transactions with invalid dates."""

        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "invalid-date", "quantity_sold": "5"},
        ]

        result, processed, quality = aggregate_sales(sales, inventory)

        self.assertEqual(result, {})  # No aggregation
        self.assertEqual(processed, 0)
        self.assertEqual(quality["invalid_dates"], 1)


    def test_negative_quantity_ignored(self):
        """Should ignore transactions with negative quantity."""

        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "2024-04-10", "quantity_sold": "-5"},
        ]

        result, processed, quality = aggregate_sales(sales, inventory)

        self.assertEqual(result, {})
        self.assertEqual(processed, 0)
        self.assertEqual(quality["negative_quantities"], 1)


    def test_unknown_product_ignored(self):
        """Should ignore transactions for products not present in inventory."""

        inventory = {"1": {}}
        sales = [
            {"product_id": "999", "transaction_date": "2024-04-10", "quantity_sold": "5"},
        ]

        result, processed, quality = aggregate_sales(sales, inventory)

        self.assertEqual(result, {})
        self.assertEqual(processed, 0)
        self.assertEqual(quality["unknown_products"], 1)