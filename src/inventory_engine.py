def reconcile_inventory(inventory, aggregated_sales):
    results = []

    for product_id, data in inventory.items():
        total_sold = aggregated_sales.get(product_id, 0)
        final_stock = data["current_stock"] - total_sold

        stock_error = False
        if final_stock < 0:
            final_stock = 0
            stock_error = True

        if final_stock == 0:
            status = "OUT_OF_STOCK"
        elif 1 <= final_stock <= 10:
            status = "LOW_STOCK"
        else:
            status = "AVAILABLE"

        total_sales_value = total_sold * data["unit_price"]

        results.append({
            "product_id": product_id,
            "product_name": data["product_name"],
            "category": data["category"],
            "current_stock": data["current_stock"],
            "total_sold_quantity": total_sold,
            "final_stock": final_stock,
            "stock_status": status,
            "total_sales_value": total_sales_value,
        })

    return results