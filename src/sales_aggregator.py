from datetime import datetime
import logging

APRIL_YEAR = 2024
APRIL_MONTH = 4

def aggregate_sales(sales_data, inventory):
    aggregated = {}
    processed_transactions = 0

    for sale in sales_data:
        try:
            date_obj = datetime.strptime(sale["transaction_date"], "%Y-%m-%d")
        except ValueError:
            logging.warning("Invalid date skipped", extra={"sale": sale})
            continue

        if date_obj.year != APRIL_YEAR or date_obj.month != APRIL_MONTH:
            continue

        quantity = int(sale["quantity_sold"])
        if quantity < 0:
            logging.warning("Negative quantity ignored", extra={"sale": sale})
            continue

        product_id = sale["product_id"]

        if product_id not in inventory:
            logging.warning("Unknown product ID", extra={"sale": sale})
            continue

        aggregated[product_id] = aggregated.get(product_id, 0) + quantity
        processed_transactions += 1

    return aggregated, processed_transactions