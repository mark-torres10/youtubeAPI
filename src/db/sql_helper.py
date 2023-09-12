"""SQL helper utility functions."""
from dataclasses import dataclass
from datetime import datetime
import sqlite3
from sqlite3 import Error
from typing import List, Dict


from lib.constants import SQLITE_ENGINE

def create_connection():
    """Create a database connection to SQLite (create the database if it doesn't exist)."""
    conn = None
    try:
        conn = sqlite3.connect(SQLITE_ENGINE)
        print(f"Connected to SQLite database: {SQLITE_ENGINE}")
        return conn
    except Error as e:
        print(e)
    return conn


def execute_query(conn, query):
    """Execute a SQL query."""
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor
    except Error as e:
        print(e)
        return None


def execute_insert(conn, query, data):
    """Insert data into the database."""
    try:
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
        return None


def execute_read_query(conn, query):
    """Execute a SELECT query and fetch results."""
    cursor = execute_query(conn, query)
    if cursor:
        return cursor.fetchall()
    return None


def close_connection(conn):
    """Close the database connection."""
    if conn:
        conn.close()
        print("SQLite database connection closed")
