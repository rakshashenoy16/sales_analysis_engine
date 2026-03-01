def reconcile_inventory(inventory, aggregated_sales):
    results = []

    for product_id, data in inventory.items():
        total_sold = aggregated_sales.get(product_id, 0)
        current_stock = data["current_stock"]

        final_stock = current_stock - total_sold

        if final_stock < 0:
            final_stock = 0

        ## Stock Status Logic (your original style kept)
        if final_stock == 0:
            status = "OUT_OF_STOCK"
        elif 1 <= final_stock <= 10:
            status = "LOW_STOCK"
        else:
            status = "AVAILABLE"

        total_sales_value = total_sold * data["unit_price"]

        # Stock Utilization %
        if current_stock > 0:
            stock_utilization_percentage = round(
                (total_sold / current_stock) * 100, 2
            )
        else:
            stock_utilization_percentage = 0.0

        # Estimated Days Until Stockout (April = 30 days)
        if total_sold > 0:
            avg_daily_sales = total_sold / 30
            if avg_daily_sales > 0:
                estimated_days_until_stockout = round(
                    final_stock / avg_daily_sales, 2
                )
            else:
                estimated_days_until_stockout = None
        else:
            estimated_days_until_stockout = None

        results.append({
            "product_id": product_id,
            "product_name": data["product_name"],
            "category": data["category"],
            "current_stock": current_stock,
            "total_sold_quantity": total_sold,
            "final_stock": final_stock,
            "stock_status": status,
            "total_sales_value": total_sales_value,
            "stock_utilization_percentage": stock_utilization_percentage,
            "estimated_days_until_stockout": estimated_days_until_stockout,
        })

    return results