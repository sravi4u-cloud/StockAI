from watchlist.watchlist import view_watchlist
from data.downloader import get_live_price

def get_price_alerts():
    alerts = []

    rows = view_watchlist()

    for row in rows:
        symbol = row[0]
        target_price = row[1]

        live_price = get_live_price(symbol)

        if live_price is not None:
            if live_price <= target_price:
                alert = "BUY NOW"
            else:
                alert = "WAIT"

            alerts.append({
                "symbol": symbol,
                "live_price": round(live_price, 2),
                "target_price": target_price,
                "alert": alert
            })

    return alerts

