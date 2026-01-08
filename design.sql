- 1. Companies Table
    CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );

-- 2. Warehouses Table
-- Relationship: One Company -> Many Warehouses.
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

-- 3. Suppliers Table                                                                                                                      -- Stores vendor details for reordering.
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

-- 4. Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER REFERENCES suppliers(id),
    sku VARCHAR(50) UNIQUE NOT NULL, 
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL, -- DECIMAL type used for financial precision
    low_stock_threshold INTEGER DEFAULT 10, 
    is_bundle BOOLEAN DEFAULT FALSE,
    last_sold_at TIMESTAMP
);

-- 5. Inventory Table (Junction Table)
-- Tracks 'quantity' per location.
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    warehouse_id INTEGER REFERENCES warehouses(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    UNIQUE(warehouse_id, product_id)   -- Constraint: Prevent duplicate records
);

-- 6. Bundle_Items Table
-- Recursive Relationship: Defines which products make up a bundle.
CREATE TABLE bundle_items (
    id SERIAL PRIMARY KEY,
    bundle_id INTEGER REFERENCES products(id),    
    component_id INTEGER REFERENCES products(id), 
    quantity_needed INTEGER NOT NULL
);
