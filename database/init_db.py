import sqlite3
import os

# Create database folder if it doesn't exist
os.makedirs("database", exist_ok=True)

DB_PATH = "database/stockai.db"

def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create stocks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        symbol TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        industry TEXT,
        market_cap REAL,
        current_price REAL,
        pe_ratio REAL,
        roe REAL,
        last_updated TEXT
    )
    """)

    # Create portfolio table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        quantity INTEGER,
        buy_price REAL,
        buy_date TEXT
    )
    """)

    # Create watchlist table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        target_price REAL,
        alert_enabled INTEGER DEFAULT 1
    )
    """)

    # Create screener results table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS screener_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        price REAL,
        pe_ratio REAL,
        roe REAL,
        score REAL,
        screened_at TEXT
    )
    """)
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()

    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()