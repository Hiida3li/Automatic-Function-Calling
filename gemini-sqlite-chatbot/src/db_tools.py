import sqlite3
import os

db_file = os.path.join(os.path.dirname(__file__), '..', 'database', 'sample.db')
db_conn = sqlite3.connect(db_file)

def list_tables() -> list[str]:
    """Retrieve all table names."""
    cursor = db_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [t[0] for t in cursor.fetchall()]

def describe_table(table_name: str) -> list[tuple[str, str]]:
    """Get table schema."""
    cursor = db_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [(col[1], col[2]) for col in cursor.fetchall()]

def execute_query(sql: str) -> list[list[str]]:
    """Execute SQL query."""
    cursor = db_conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def plot_orders_per_stuff():
    """Plot the number of orders handled by each staff member."""
    sql= """
    SELECT s.name, COUNT(o.order_id)
    from orders o
    JOIN staff s ON o.staff_id = s.staff_id
    GROUP BY s.name
    ORDER BY COUNT(o.order_id) DESC
    """
