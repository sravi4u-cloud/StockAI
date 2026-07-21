import yfinance as yf

def get_live_price(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")

        # Get latest closing price
        hist = stock.history(period="1d")

        if not hist.empty:
            return round(hist["Close"].iloc[-1], 2)

        return None

    except Exception as e:
        print("Error fetching price:", e)
        return None

def get_fundamentals(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")
        info = stock.info

        return {
            "eps": info.get("trailingEps", "N/A"),
            "roe": round(info.get("returnOnEquity", 0) * 100, 2)
                    if info.get("returnOnEquity") else "N/A",
            "pe": info.get("trailingPE", "N/A"),
            "book_value": info.get("bookValue", "N/A"),
            "market_cap": info.get("marketCap", "N/A")
        }

    except Exception as e:
        print("Error fetching fundamentals:", e)
        return None
