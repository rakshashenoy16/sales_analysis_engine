import csv
import logging

def load_inventory(file_path):
    inventory = {}

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            inventory[row["product_id"]] = {
                "product_name": row["product_name"],
                "current_stock": int(row["current_stock"]),
                "unit_price": float(row["unit_price"]),
                "category": row["category"],
            }
    return inventory


def load_sales(file_path):
    sales = []

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sales.append(row)

    return sales