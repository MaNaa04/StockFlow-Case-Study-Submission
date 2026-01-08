@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json

    # 1. Safe Input Extraction (Fixes "Trusting User Input")
    name = data.get('name')
    sku = data.get('sku')
    price = data.get('price')
    warehouse_id = data.get('warehouse_id')
    initial_quantity = data.get('initial_quantity')

    if price is not None and price < 0:
        return {"error": "Price cannot be negative"}, 400

    # 2. Check for Duplicate SKU (Fixes "Integrity Error")
    existing_product = Product.query.filter_by(sku=sku).first()
    if existing_product:
        return {"error": "Product with this SKU already exists"},400 

    try:
        # 3. Create Product (Do not commit yet!)
        product = Product(
            name=name,
            sku=sku,
            price=price,
            warehouse_id=warehouse_id
        )
        db.session.add(product)
        db.session.flush()  #it will ensure that ID is created before the commit.
      
         # 4. Create Inventory
        inventory = Inventory(
            product_id=product.id,
            warehouse_id = data.get('warehouse_id'),
            quantity = data.get('initial_quantity')
        )
        db.session.add(inventory)
        

        # 5. Atomic Commit (Fixes the "Two Commits" problem)
        # This saves BOTH the Product and Inventory at the same exact time.
        db.session.commit()

        return {"message": "Product created", "product_id": product.id}, 201

    except Exception as e:
        db.session.rollback() # Undo everything if anything fails
        return {"error": str(e)}, 500

