# Inventory Reconciliation & Sales Analysis Engine

##  Project Overview

This project implements an Inventory Reconciliation & Sales Analysis Engine in Python.

The system processes inventory and sales transaction data, applies business rules,
reconciles stock levels, detects stock issues, and generates analytical reports.

Developed as part of a Software/Data Engineering Internship assignment.



## Business Objective

As an Inventory Operations Engineer,
I want to process inventory and sales transactions,
So that I can:

- Reconcile stock levels
- Identify low-stock and out-of-stock products
- Generate sales summaries
- Handle invalid data safely
- Produce validated reports



## Business Rules Implemented

### Sales Filtering
- Only April 2024 transactions considered
- Invalid dates are logged and skipped
- Negative quantities are ignored
- Unknown product IDs are logged

### Inventory Reconciliation
final_stock = current_stock - total_sold_quantity


- If final_stock < 0 → set to 0
- Stock status rules:
  - 0 → OUT_OF_STOCK
  - 1–10 → LOW_STOCK
  - >10 → AVAILABLE

### Transformations Added
- total_sold_quantity
- final_stock
- stock_status
- total_sales_value



## Output Files

### inventory_reconciliation.csv
Contains:
- product_id
- product_name
- category
- current_stock
- total_sold_quantity
- final_stock
- stock_status
- total_sales_value

### sales_summary.json
Contains:
- total_products
- total_transactions_processed
- total_sales_value
- low_stock_products
- out_of_stock_products



## How To Run

### Install dependencies


pip install -r requirements.txt


### Run Application

From project root:


python -m src.main




##  Running Unit Tests


python -m unittest discover tests




## Running Coverage (80%+ Required)


coverage run -m unittest discover tests
coverage report -m


Optional HTML report:


coverage html




##  Error Handling & Logging

- Invalid transaction dates are logged
- Negative sales quantities ignored
- Unknown product IDs logged
- Application does not crash on bad data
- Logs stored in `logs/inventory.log`



##  Edge Cases Handled

- Stock never becomes negative
- Transactions outside April 2024 ignored
- Multiple sales aggregated correctly
- Missing/invalid records handled safely



##  Technologies Used

- Python 3
- unittest
- coverage
- logging
- csv / json

