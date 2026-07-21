from database.database import get_connection

def add_to_watchlist(symbol, target_price):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO watchlist (symbol, target_price) VALUES (?, ?)",
        (symbol.upper(), target_price)
    )

    conn.commit()
    conn.close()

def view_watchlist():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol, target_price FROM watchlist")
    rows = cursor.fetchall()

    conn.close()

    return rows