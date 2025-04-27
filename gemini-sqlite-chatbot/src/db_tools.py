import sqlite3
import pandas as pd

def list_tables():
    """List all tables in the database"""
    conn = sqlite3.connect('../database/sample.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def describe_table(table_name):
    """Get the schema of a specific table"""
    conn = sqlite3.connect('../database/sample.db')
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    conn.close()
    
    schema = []
    for col in columns:
        schema.append({
            'column_name': col[1],
            'data_type': col[2],
            'nullable': not col[3],
            'primary_key': bool(col[5])
        })
    return schema

def execute_query(sql):
    """Execute a SQL query and return results"""
    conn = sqlite3.connect('../database/sample.db')
    try:
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df.to_dict('records')
    except Exception as e:
        conn.close()
        return f"Error: {str(e)}"
        