# StockFlow Backend Case Study

This repository contains my solution for the Backend Engineering Internship Case Study.

**📄 [Click Here to View the Case Study Document (Part 1, 2, & 3)](https://docs.google.com/document/d/1uG44KOU58s5pUZm8kD3_88PJ-8sjcaoaNABCAlEOcZI/edit?usp=sharing)**

## Structure

* **part1_debugging.py**: Corrected API endpoint for product creation. 
    * *Fixes:* Implemented atomic transactions, added input validation, and fixed floating-point price handling.
    
* **part2_schema.sql**: Database schema design (SQL DDL).
    * *Features:* Handles multi-warehouse inventory, supplier relationships, and recursive product bundles.
    
* **part3_api.py**: Implementation of the Low Stock Alert API.
    * *Logic:* Filters products based on stock thresholds and recent sales activity (last 30 days).

## Assumptions
Key assumptions made during design:
1.  **Sales Activity:** Assumed (created) a `last_sold_at` column exists on products to identify "dead stock."

2.  **Currency:** Defaulted to USD for all prices.