import csv
import json
from datetime import datetime


def write_inventory_report(results, file_path):
    """
    Writes enhanced inventory reconciliation report.
    Adds:
    - stock_utilization_percentage
    - estimated_days_until_stockout
    """

    # Add new calculated fields without modifying core logic
    enriched_results = []

    for row in results:
        new_row = row.copy()

        current_stock = row["current_stock"]
        sold = row["total_sold_quantity"]
        final_stock = row["final_stock"]

        # Stock utilization %
        if current_stock > 0:
            new_row["stock_utilization_percentage"] = round((sold / current_stock) * 100, 2)
        else:
            new_row["stock_utilization_percentage"] = 0

        # Estimated days until stockout (based on April = 30 days)
        daily_avg_sales = sold / 30 if sold > 0 else 0

        if daily_avg_sales > 0:
            new_row["estimated_days_until_stockout"] = round(final_stock / daily_avg_sales, 2)
        else:
            new_row["estimated_days_until_stockout"] = None

        enriched_results.append(new_row)

    fieldnames = [
        "product_id",
        "product_name",
        "category",
        "current_stock",
        "total_sold_quantity",
        "final_stock",
        "stock_status",
        "total_sales_value",
        "stock_utilization_percentage",
        "estimated_days_until_stockout",
    ]

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched_results)


def write_summary(results, total_transactions, file_path):
    """
    Writes summary report with metadata.
    """

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
        "run_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "engine_version": "2.0.0",
    }

    with open(file_path, "w") as f:
        json.dump(summary, f, indent=4)


def write_category_summary(results, file_path):
    """
    Writes category-level aggregated summary.
    """

    category_data = {}

    for row in results:
        category = row["category"]

        if category not in category_data:
            category_data[category] = {
                "total_products": 0,
                "total_units_sold": 0,
                "total_revenue": 0,
                "total_stock_remaining": 0,
            }

        category_data[category]["total_products"] += 1
        category_data[category]["total_units_sold"] += row["total_sold_quantity"]
        category_data[category]["total_revenue"] += row["total_sales_value"]
        category_data[category]["total_stock_remaining"] += row["final_stock"]

    fieldnames = [
        "category",
        "total_products",
        "total_units_sold",
        "total_revenue",
        "total_stock_remaining",
    ]

    with open(file_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for category, data in category_data.items():
            row = {"category": category}
            row.update(data)
            writer.writerow(row)


def write_data_quality_report(quality_report, file_path):
    
    ##Writes data quality metrics.

    with open(file_path, "w") as f:
        json.dump(quality_report, f, indent=4)