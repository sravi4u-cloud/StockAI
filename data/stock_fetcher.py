import yfinance as yf
from datetime import datetime

def fetch_stock_data(symbol):
    try:
        # Ensure NSE suffix
        if not symbol.endswith(".NS"):
            symbol += ".NS"

        stock = yf.Ticker(symbol)
        info = stock.info

        # If Yahoo returns no data
        if not info or info.get("currentPrice") is None:
            print(f"Could not fetch data for {symbol}")
            return None

        stock_data = {
            "symbol": symbol,
            "company_name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "current_price": info.get("currentPrice", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "roe": info.get("returnOnEquity", 0),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        return stock_data

    except Exception:
        return None