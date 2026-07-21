from database.database import get_connection
from data.downloader import get_live_price

# Basic sector mapping
SECTOR_MAP = {
    "HAL": "Defence",
    "BEL": "Defence",
    "SBIN": "Banking",
    "HDFCBANK": "Banking",
    "AUBANK": "Banking",
    "BAJFINANCE": "Financial Services",
    "CAMS": "Financial Services",
    "ICICIGI": "Insurance",
    "POLYCAB": "Electricals",
    "ULTRACEMCO": "Cement",
    "INFY": "IT",
    "WIPRO": "IT",
    "TATAELXSI": "IT",
    "ETERNAL": "Consumer",
    "DMART": "Retail",
}

def get_portfolio_analytics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol, quantity, buy_price FROM portfolio")
    rows = cursor.fetchall()

    conn.close()

    total_value = 0
    total_cost = 0
    gainers = []
    losers = []
    sector_allocation = {}

    for row in rows:
        symbol, qty, buy_price = row
        live_price = get_live_price(symbol)

        if live_price:
            current_value = qty * live_price
            cost = qty * buy_price
            pl = current_value - cost

            total_value += current_value
            total_cost += cost

            # Gainers and losers
            gainers.append((symbol, pl))
            losers.append((symbol, pl))

            # Sector allocation
            sector = SECTOR_MAP.get(symbol.split("-")[0], "Others")
            sector_allocation[sector] = sector_allocation.get(sector, 0) + current_value

    total_pl = total_value - total_cost

    # Sort gainers and losers
    gainers = sorted(gainers, key=lambda x: x[1], reverse=True)[:5]
    losers = sorted(losers, key=lambda x: x[1])[:5]

    return {
        "total_value": round(total_value, 2),
        "total_pl": round(total_pl, 2),
        "gainers": gainers,
        "losers": losers,
        "sector_allocation": sector_allocation,
    }