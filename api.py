from datetime import datetime, timedelta
from flask import app
from flask import jsonify


@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):

    # 1. Define "Recent Sales" Window
    # Assumption: We only care about items sold in the last 30 days
    thirty_days_ago = datetime.now(datetime.timezone.utc) - timedelta(days=30)

    # 2. Database Query
    # need to join 4 tables to get all the data at once: 
    # Inventory -> Product -> Warehouse -> Supplier
    # Logic: Find items where stock < threshold AND sold recently

    results = db.session.query(Inventory, Product, Warehouse, Supplier)\
        .join(Product, Inventory.product_id == Product.id)\
        .join(Warehouse, Inventory.warehouse_id == Warehouse.id)\
        .join(Supplier, Product.supplier_id == Supplier.id)\
        .filter(Warehouse.company_id == company_id)\
        .filter(Product.last_sold_at >= thirty_days_ago)\
        .filter(Inventory.quantity < Product.low_stock_threshold)\
        .all()

    # 3. Format the Output
    alerts_list = []
    for inventory, product, warehouse, supplier in results:
        # LOGIC CHECK 1: Is the stock low?
        # We compare current quantity against the product's specific threshold

        if inventory.quantity < product.low_stock_threshold: 
            # LOGIC CHECK 2: Was it sold recently?
            # if product.last_sold_at >= thirty_days_ago :
            #     # Calculate days until empty 
            #     days_left = 0
            #     if inventory.quantity > 0:
            #         days_left = inventory.quantity

            # Create the alert dictionary
            alert_data = {
                "product_id": product.id,
                "product_name": product.name,
                "sku": product.sku,
                "warehouse_id": warehouse.id,
                "warehouse_name": warehouse.name,
                "current_stock": inventory.quantity,
                "threshold": product.low_stock_threshold,
                "days_until_stockout": days_left,
                "supplier": {
                    "id": supplier.id,
                    "name": supplier.name,
                    "contact_email": supplier.email
                }
            }
            alerts_list.append(alert_data)

    # Return the Result
    return jsonify({
        "alerts": alerts_list,
        "total_alerts": len(alerts_list)
    })