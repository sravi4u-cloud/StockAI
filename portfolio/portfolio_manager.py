
from database.db_manager import get_portfolio
from database.db_manager import (
    add_to_portfolio,
    get_portfolio,
    delete_from_portfolio
)
from data.stock_fetcher import fetch_stock_data
from datetime import datetime

import sqlite3

def add_holding():
    symbol = input("Enter NSE stock symbol: ").upper() + ".NS"
    quantity = int(input("Enter quantity: "))
    buy_price = float(input("Enter buy price: ₹"))

    buy_date = datetime.now().strftime("%Y-%m-%d")

    add_to_portfolio(symbol, quantity, buy_price, buy_date)
    print("Stock added to portfolio successfully!")

def view_portfolio():
    holdings = get_portfolio()

    if not holdings:
        print("Portfolio is empty.")
        return
    

    total_invested = 0
    total_current = 0

    print("\n=== PORTFOLIO ===")

    for holding in holdings:
        holding_id, symbol, quantity, buy_price, buy_date = holding

        stock_data = fetch_stock_data(symbol)
        current_price = stock_data["current_price"] if stock_data else 0

        invested = quantity * buy_price
        current_value = quantity * current_price
        pnl = current_value - invested

        total_invested += invested
        total_current += current_value

        print(f"\nID: {holding_id}")
        print(f"Stock: {symbol}")
        print(f"Quantity: {quantity}")
        print(f"Buy Price: ₹{buy_price}")
        print(f"Current Price: ₹{current_price}")
        print(f"Invested: ₹{invested}")
        print(f"Current Value: ₹{current_value}")
        print(f"P&L: ₹{pnl:.2f}")

    print("\n=== SUMMARY ===")
    print(f"Total Invested: ₹{total_invested:.2f}")
    print(f"Current Value: ₹{total_current:.2f}")
    print(f"Total P&L: ₹{(total_current - total_invested):.2f}")

def remove_holding():
    view_portfolio()
    holding_id = int(input("\nEnter Holding ID to delete: "))

    delete_from_portfolio(holding_id)
    print("Holding deleted successfully!")

    import sqlite3

DB_PATH = "database/stockai.db"

def delete_holding(holding_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM portfolio WHERE id = ?", (holding_id,))

    conn.commit()
    conn.close()

    print("Holding deleted successfully!")