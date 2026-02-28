import logging
from src.loader import load_inventory, load_sales
from src.sales_aggregator import aggregate_sales
from src.inventory_engine import reconcile_inventory
from src.reporter import write_inventory_report, write_summary

logging.basicConfig(
    filename="logs/inventory.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    inventory = load_inventory("data/inventory.csv")
    sales = load_sales("data/sales_transactions.csv")

    aggregated_sales, total_transactions = aggregate_sales(sales, inventory)
    results = reconcile_inventory(inventory, aggregated_sales)

    write_inventory_report(results, "inventory_reconciliation.csv")
    write_summary(results, total_transactions, "sales_summary.json")

    print("Processing completed successfully!")

if __name__ == "__main__":
    main()