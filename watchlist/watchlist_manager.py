from database.db_manager import (
    add_to_watchlist,
    get_watchlist,
    delete_from_watchlist
)
from data.stock_fetcher import fetch_stock_data

def add_stock():
    symbol = input("Enter NSE stock symbol: ").upper() + ".NS"
    target_price = float(input("Enter target buy price: ₹"))

    add_to_watchlist(symbol, target_price)
    print("Stock added to watchlist successfully!")

def view_watchlist():
    watchlist = get_watchlist()

    if not watchlist:
        print("Watchlist is empty.")
        return

    print("\n=== WATCHLIST ===")

    for item in watchlist:
        watchlist_id, symbol, target_price, alert_enabled = item

        stock_data = fetch_stock_data(symbol)
        current_price = stock_data["current_price"] if stock_data else 0

        print(f"\nID: {watchlist_id}")
        print(f"Stock: {symbol}")
        print(f"Current Price: ₹{current_price}")
        print(f"Target Price: ₹{target_price}")

        # Price alert
        if current_price <= target_price:
            print("ALERT: Stock has reached your target price!")

def remove_stock():
    view_watchlist()
    watchlist_id = int(input("\nEnter Watchlist ID to delete: "))

    delete_from_watchlist(watchlist_id)
    print("Stock removed from watchlist successfully!")