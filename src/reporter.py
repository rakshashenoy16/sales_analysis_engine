import csv
import json

def write_inventory_report(results, file_path):
    fieldnames = [
        "product_id",
        "product_name",
        "category",
        "current_stock",
        "total_sold_quantity",
        "final_stock",
        "stock_status",
        "total_sales_value",
    ]

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def write_summary(results, total_transactions, file_path):
    total_products = len(results)
    total_sales_value = sum(r["total_sales_value"] for r in results)
    low_stock = sum(1 for r in results if r["stock_status"] == "LOW_STOCK")
    out_of_stock = sum(1 for r in results if r["stock_status"] == "OUT_OF_STOCK")

    summary = {
        "total_products": total_products,
        "total_transactions_processed": total_transactions,
        "total_sales_value": total_sales_value,
        "low_stock_products": low_stock,
        "out_of_stock_products": out_of_stock,
    }

    with open(file_path, "w") as f:
        json.dump(summary, f, indent=4)