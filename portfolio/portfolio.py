from database.database import get_connection

def add_stock(symbol, quantity, buy_price):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO portfolio (symbol, quantity, buy_price) VALUES (?, ?, ?)",
        (symbol.upper(), quantity, buy_price)
    )

    conn.commit()
    conn.close()

def view_portfolio():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol, quantity, buy_price FROM portfolio")
    rows = cursor.fetchall()

    conn.close()

    return rows
