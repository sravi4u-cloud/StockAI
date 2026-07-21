from database.database import get_connection
from data.downloader import get_live_price

def get_recommendations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol, quantity, buy_price FROM portfolio")
    rows = cursor.fetchall()
    conn.close()

    recommendations = []
    total_value = 0

    # First calculate total portfolio value
    portfolio_data = []
    for symbol, qty, buy_price in rows:
        live_price = get_live_price(symbol)

        if live_price:
            current_value = qty * live_price
            total_value += current_value
            portfolio_data.append((symbol, qty, buy_price, live_price, current_value))

    # Generate recommendations
    for symbol, qty, buy_price, live_price, current_value in portfolio_data:
        cost_value = qty * buy_price
        pl = current_value - cost_value
        pl_percent = (pl / cost_value) * 100 if cost_value > 0 else 0
        weight = (current_value / total_value) * 100

        # Recommendation logic
        if pl_percent < -40:
            recommendation = "SELL"
            reason = "Heavy loss, reassess fundamentals"
            risk = "High"
        elif pl_percent < -15:
            recommendation = "HOLD"
            reason = "Loss position, wait for recovery"
            risk = "Medium"
        elif pl_percent > 30 and weight < 5:
            recommendation = "BUY"
            reason = "Strong performer, room to add"
            risk = "Low"
        elif pl_percent > 15:
            recommendation = "HOLD"
            reason = "Good profit, continue holding"
            risk = "Low"
        else:
            recommendation = "HOLD"
            reason = "Stable position"
            risk = "Medium"

        recommendations.append({
            "symbol": symbol,
            "live_price": round(live_price, 2),
            "pl_percent": round(pl_percent, 2),
            "weight": round(weight, 2),
            "recommendation": recommendation,
            "reason": reason,
            "risk": risk
        })

    # Sort by recommendation priority
    recommendations = sorted(
        recommendations,
        key=lambda x: (x["recommendation"] == "SELL", x["pl_percent"]),
        reverse=True
    )

    return recommendations
