import sqlite3
import random
from datetime import datetime, timedelta

# This script creates a sample SQLite database with products, staff, and orders

def create_database():
    # Connect to SQLite database (it will create it if it doesn't exist)
    conn = sqlite3.connect('sample.db')
    cursor = conn.cursor()
    
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT,
        stock INTEGER DEFAULT 0
    )
    ''')
    
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        hire_date DATE
    )
    ''')
    
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        staff_id INTEGER,
        quantity INTEGER,
        order_date DATE,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
    )
    ''')
    
    # Insert sample data
    # Sample products
    products = [
        ('Laptop', 999.99, 'Electronics', 50),
        ('Smartphone', 599.99, 'Electronics', 100),
        ('Headphones', 79.99, 'Electronics', 200),
        ('Desk Chair', 149.99, 'Furniture', 30),
        ('Coffee Maker', 89.99, 'Appliances', 40),
        ('Water Bottle', 19.99, 'Accessories', 150),
        ('Notebook', 4.99, 'Stationery', 300),
        ('Backpack', 49.99, 'Accessories', 75)
    ]
    
    cursor.executemany('''
    INSERT INTO products (name, price, category, stock) 
    VALUES (?, ?, ?, ?)
    ''', products)
    
    # Sample staff
    staff = [
        ('Alice Johnson', 'Sales Associate', '2023-01-15'),
        ('Bob Smith', 'Manager', '2022-05-20'),
        ('Carol White', 'Sales Associate', '2023-03-10'),
        ('David Brown', 'Technician', '2022-11-01'),
        ('Micheal Hilx', 'Engineer', '2023-11-01')

    ]
    
    cursor.executemany('''
    INSERT INTO staff (name, position, hire_date) 
    VALUES (?, ?, ?)
    ''', staff)
    
    # Generate random orders
    orders = []
    for _ in range(20):
        product_id = random.randint(1, len(products))
        staff_id = random.randint(1, len(staff))
        quantity = random.randint(1, 5)
        # Random date within the last 30 days
        days_ago = random.randint(0, 30)
        order_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        orders.append((product_id, staff_id, quantity, order_date))
    
    cursor.executemany('''
    INSERT INTO orders (product_id, staff_id, quantity, order_date) 
    VALUES (?, ?, ?, ?)
    ''', orders)
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database created successfully!")
    print("Created tables: products, staff, orders")
    print(f"Inserted {len(products)} products, {len(staff)} staff members, and {len(orders)} orders")

if __name__ == "__main__":
    create_database()
    