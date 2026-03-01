import csv
import logging


def load_inventory(file_path):
    """
    Loads inventory data from a CSV file and returns
    a dictionary keyed by product_id.

    Expected columns:
    product_id, product_name, current_stock, unit_price, category
    """
    inventory = {}

    # Open inventory CSV file
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        # Read each row and build inventory dictionary
        for row in reader:
            inventory[row["product_id"]] = {
                "product_name": row["product_name"],
                "current_stock": int(row["current_stock"]),  # Convert to integer
                "unit_price": float(row["unit_price"]),      # Convert to float
                "category": row["category"],
            }

    return inventory


def load_sales(file_path):
    """
    Loads sales transaction data from a CSV file
    and returns a list of transaction dictionaries.

    No validation is performed here — validation
    happens in the sales_aggregator module.
    """
    sales = []

    # Open sales transactions CSV file
    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        # Append each transaction row as dictionary
        for row in reader:
            sales.append(row)

    return sales