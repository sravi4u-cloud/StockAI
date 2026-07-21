from database.database import get_connection
from data.downloader import get_live_price

def get_advanced_analytics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol, quantity, buy_price FROM portfolio")
    rows = cursor.fetchall()
    conn.close()

    holdings = []
    total_value = 0

    # Calculate current value of each holding
    for symbol, qty, buy_price in rows:
        live_price = get_live_price(symbol)

        if live_price:
            current_value = qty * live_price
            total_value += current_value

            holdings.append({
                "symbol": symbol,
                "current_value": current_value,
                "buy_value": qty * buy_price
            })

    # Calculate portfolio weights
    for h in holdings:
        h["weight"] = (h["current_value"] / total_value) * 100

    # Sort by weight
    holdings = sorted(holdings, key=lambda x: x["weight"], reverse=True)

    # Concentration risk = Top 10 holdings percentage
    top_10_weight = sum(h["weight"] for h in holdings[:10])

    # Diversification score
    num_holdings = len(holdings)
    if num_holdings >= 30 and top_10_weight < 50:
        diversification_score = 9
    elif num_holdings >= 20 and top_10_weight < 60:
        diversification_score = 8
    elif num_holdings >= 15 and top_10_weight < 70:
        diversification_score = 7
    else:
        diversification_score = 5

    # Rebalancing suggestions
    rebalance = []
    for h in holdings[:10]:
        if h["weight"] > 8:
            rebalance.append(
                f"Reduce {h['symbol']} (weight: {round(h['weight'],2)}%)"
            )

    return {
        "total_value": round(total_value, 2),
        "diversification_score": diversification_score,
        "concentration_risk": round(top_10_weight, 2),
        "top_holdings": holdings[:10],
        "rebalance": rebalance
    }