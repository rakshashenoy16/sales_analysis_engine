import unittest
from src.sales_aggregator import aggregate_sales

class SalesAggregationTests(unittest.TestCase):

    def test_multiple_sales_aggregation(self):
        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "2024-04-10", "quantity_sold": "5"},
            {"product_id": "1", "transaction_date": "2024-04-15", "quantity_sold": "3"},
        ]
        result, _ = aggregate_sales(sales, inventory)
        self.assertEqual(result["1"], 8)

    def test_invalid_transaction_date(self):
        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "invalid-date", "quantity_sold": "5"},
        ]
        result, _ = aggregate_sales(sales, inventory)
        self.assertEqual(result, {})

    def test_negative_quantity_ignored(self):
        inventory = {"1": {}}
        sales = [
            {"product_id": "1", "transaction_date": "2024-04-10", "quantity_sold": "-5"},
        ]
        result, _ = aggregate_sales(sales, inventory)
        self.assertEqual(result, {})