import sqlite3

DB_PATH = "database/stockai.db"

# ---------------- STOCKS ----------------

def save_stock(stock_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO stocks
    (symbol, company_name, sector, industry, market_cap, current_price, pe_ratio, roe, last_updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        stock_data["symbol"],
        stock_data["company_name"],
        stock_data["sector"],
        stock_data["industry"],
        stock_data["market_cap"],
        stock_data["current_price"],
        stock_data["pe_ratio"],
        stock_data["roe"],
        stock_data["last_updated"]
    ))

    conn.commit()
    conn.close()

# ---------------- PORTFOLIO ----------------

def add_to_portfolio(symbol, quantity, buy_price, buy_date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO portfolio (symbol, quantity, buy_price, buy_date)
    VALUES (?, ?, ?, ?)
    """, (symbol, quantity, buy_price, buy_date))

    conn.commit()
    conn.close()

def get_portfolio():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM portfolio")
    holdings = cursor.fetchall()

    conn.close()
    return holdings

def delete_from_portfolio(holding_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM portfolio WHERE id = ?", (holding_id,))

    conn.commit()
    conn.close()

# ---------------- WATCHLIST ----------------

def add_to_watchlist(symbol, target_price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO watchlist (symbol, target_price)
    VALUES (?, ?)
    """, (symbol, target_price))

    conn.commit()
    conn.close()

def get_watchlist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM watchlist")
    watchlist = cursor.fetchall()

    conn.close()
    return watchlist

def delete_from_watchlist(watchlist_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM watchlist WHERE id = ?", (watchlist_id,))

    conn.commit()
    conn.close()