import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Database connection
db_file = "sample.db"
db_conn = sqlite3.connect(db_file)

def list_tables() -> list[str]:
    """Retrieve the names of all tables in the database."""
    # Include print logging statements so you can see when functions are being called.
    print(' - DB CALL: list_tables()')
    
    cursor = db_conn.cursor()
    
    # Fetch the table names.
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    tables = cursor.fetchall()
    return [t[0] for t in tables]

def describe_table(table_name: str) -> list[tuple[str, str]]:
    """Look up the table schema.
    
    Returns:
      List of columns, where each entry is a tuple of (column, type).
    """
    print(f' - DB CALL: describe_table({table_name})')
    
    cursor = db_conn.cursor()
    
    cursor.execute(f"PRAGMA table_info({table_name});")
    
    schema = cursor.fetchall()
    # [column index, column name, column type, ...]
    return [(col[1], col[2]) for col in schema]

def execute_query(sql: str) -> list[list[str]]:
    """Execute an SQL statement, returning the results."""
    print(f' - DB CALL: execute_query({sql})')
    
    cursor = db_conn.cursor()
    
    cursor.execute(sql)
    return cursor.fetchall()

def plot_query_results(sql: str, plot_type: str = 'bar', 
                      title: str = None, x_column: int = 0, 
                      y_column: int = 1) -> None:
    """Execute a SQL query and plot the results.
    
    Args:
        sql: SQL query to execute
        plot_type: Type of plot ('bar', 'line', 'scatter', 'pie')
        title: Title for the plot
        x_column: Index of column to use for x-axis
        y_column: Index of column to use for y-axis
    """
    print(f' - DB CALL: plot_query_results({sql})')
    
    # Execute query and get results
    cursor = db_conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    
    # Get column names
    column_names = [description[0] for description in cursor.description]
    
    # Convert to pandas DataFrame for easier plotting
    df = pd.DataFrame(results, columns=column_names)
    
    # Create plot
    plt.figure(figsize=(10, 6))
    
    if plot_type == 'bar':
        plt.bar(df.iloc[:, x_column], df.iloc[:, y_column])
    elif plot_type == 'line':
        plt.plot(df.iloc[:, x_column], df.iloc[:, y_column], marker='o')
    elif plot_type == 'scatter':
        plt.scatter(df.iloc[:, x_column], df.iloc[:, y_column])
    elif plot_type == 'pie':
        plt.pie(df.iloc[:, y_column], labels=df.iloc[:, x_column], autopct='%1.1f%%')
    
    # Set labels and title
    if plot_type != 'pie':
        plt.xlabel(column_names[x_column])
        plt.ylabel(column_names[y_column])
    
    if title:
        plt.title(title)
    else:
        plt.title(f'{plot_type.capitalize()} Plot of {column_names[y_column]} by {column_names[x_column]}')
    
    # Rotate x-axis labels if needed
    if plot_type in ['bar', 'line', 'scatter']:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()

# Test the functions
if __name__ == "__main__":
    # Test list_tables
    print("Tables in database:")
    tables = list_tables()
    print(tables)
    print()
    
    # Test describe_table
    print("Products table schema:")
    schema = describe_table("products")
    for column, type in schema:
        print(f"  {column}: {type}")
    print()
    
    # Test execute_query
    print("First 5 products:")
    products = execute_query("SELECT * FROM products LIMIT 5")
    for product in products:
        print(product)
    print()
    
    # Test plot_query_results (optional)
    try:
        # Plot number of orders per staff member
        plot_query_results(
            sql="""
            SELECT s.name, COUNT(o.order_id) as order_count 
            FROM staff s 
            LEFT JOIN orders o ON s.staff_id = o.staff_id 
            GROUP BY s.name
            """,
            plot_type='bar',
            title='Number of Orders per Staff Member'
        )
    except Exception as e:
        print(f"Plotting failed: {e}")
        