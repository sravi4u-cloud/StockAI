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

def add_stock():
    symbol = input("Enter NSE stock symbol: ").upper() + ".NS"
    target_price = float(input("Enter target price: ₹"))
    add_to_watchlist(symbol, target_price)
    print("Stock added to watchlist successfully!")


def view_watchlist():
    watchlist = get_watchlist()

    if not watchlist:
        print("Watchlist is empty.")
        return

    print("\n=== WATCHLIST ===")
    print("ID\tSymbol\tTarget Price")

    for row in watchlist:
        print(f"{row[0]}\t{row[1]}\t₹{row[2]}")


def remove_stock():
    watchlist_id = int(input("Enter Watchlist ID to delete: "))
    remove_from_watchlist(watchlist_id)
    print("Stock removed successfully!")