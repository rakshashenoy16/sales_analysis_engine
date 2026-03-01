from datetime import datetime
import logging

APRIL_YEAR = 2024
APRIL_MONTH = 4


def aggregate_sales(sales_data, inventory):
    aggregated = {}
    processed_transactions = 0

    # NEW: Data Quality Tracking
    quality_report = {
        "invalid_dates": 0,
        "negative_quantities": 0,
        "unknown_products": 0,
        "valid_transactions": 0,
    }

    for sale in sales_data:
        try:
            date_obj = datetime.strptime(sale["transaction_date"], "%Y-%m-%d")
        except ValueError:
            logging.warning("Invalid date skipped", extra={"sale": sale})
            quality_report["invalid_dates"] += 1
            continue

        if date_obj.year != APRIL_YEAR or date_obj.month != APRIL_MONTH:
            continue

        quantity = int(sale["quantity_sold"])
        if quantity < 0:
            logging.warning("Negative quantity ignored", extra={"sale": sale})
            quality_report["negative_quantities"] += 1
            continue

        product_id = sale["product_id"]

        if product_id not in inventory:
            logging.warning("Unknown product ID", extra={"sale": sale})
            quality_report["unknown_products"] += 1
            continue

        aggregated[product_id] = aggregated.get(product_id, 0) + quantity
        processed_transactions += 1
        quality_report["valid_transactions"] += 1

    # IMPORTANT: Now returning quality_report as 3rd value
    return aggregated, processed_transactions, quality_report