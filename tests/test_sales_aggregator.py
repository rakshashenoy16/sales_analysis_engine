import unittest
from src.sales_aggregator import aggregate_sales


class SalesAggregationTests(unittest.TestCase):

    def test_multiple_sales_aggregation(self):
        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "2024-04-10", "quantity_sold": "5"},
            {"product_id": "1", "transaction_date": "2024-04-15", "quantity_sold": "3"},
        ]

        result, processed, quality = aggregate_sales(sales, inventory)

        self.assertEqual(result["1"], 8)
        self.assertEqual(processed, 2)
        self.assertEqual(quality["valid_transactions"], 2)

    def test_invalid_transaction_date(self):
        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "invalid-date", "quantity_sold": "5"},
        ]

        result, processed, quality = aggregate_sales(sales, inventory)

        self.assertEqual(result, {})
        self.assertEqual(processed, 0)
        self.assertEqual(quality["invalid_dates"], 1)

    def test_negative_quantity_ignored(self):
        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "2024-04-10", "quantity_sold": "-5"},
        ]

        result, processed, quality = aggregate_sales(sales, inventory)

        self.assertEqual(result, {})
        self.assertEqual(processed, 0)
        self.assertEqual(quality["negative_quantities"], 1)

    def test_unknown_product_ignored(self):
        inventory = {"1": {}}
        sales = [
            {"product_id": "999", "transaction_date": "2024-04-10", "quantity_sold": "5"},
        ]

        result, processed, quality = aggregate_sales(sales, inventory)

        self.assertEqual(result, {})
        self.assertEqual(processed, 0)
        self.assertEqual(quality["unknown_products"], 1)