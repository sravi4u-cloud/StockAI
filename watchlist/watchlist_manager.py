import sqlite3

DB_PATH = "database/stockai.db"

def add_to_watchlist(symbol, target_price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        target_price REAL,
        alert_enabled INTEGER DEFAULT 1
    )
    """)

    cursor.execute(
        "INSERT INTO watchlist (symbol, target_price) VALUES (?, ?)",
        (symbol.upper(), target_price)
    )

    conn.commit()
    conn.close()

def get_watchlist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM watchlist")
    watchlist = cursor.fetchall()

    conn.close()
    return watchlist

def remove_from_watchlist(watchlist_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM watchlist WHERE id = ?", (watchlist_id,))

    conn.commit()
    conn.close()