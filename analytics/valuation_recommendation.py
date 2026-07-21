import yfinance as yf
from database.database import get_connection
from data.downloader import get_live_price

def calculate_score(pe, pb, roe, roce, debt, rev_growth, profit_growth, mos):
    score = 0

    # Valuation (30 points)
    if pe > 0 and pe < 20:
        score += 15
    elif pe < 35:
        score += 10
    elif pe < 50:
        score += 5

    if pb > 0 and pb < 3:
        score += 10
    elif pb < 5:
        score += 5

    if mos > 20:
        score += 5
    elif mos > 0:
        score += 3

    # Profitability (25 points)
    if roe > 20:
        score += 15
    elif roe > 15:
        score += 10
    elif roe > 10:
        score += 5

    if roce > 20:
        score += 10
    elif roce > 15:
        score += 7
    elif roce > 10:
        score += 3

    # Growth (25 points)
    if rev_growth > 15:
        score += 12
    elif rev_growth > 10:
        score += 8
    elif rev_growth > 5:
        score += 4

    if profit_growth > 15:
        score += 13
    elif profit_growth > 10:
        score += 9
    elif profit_growth > 5:
        score += 4

    # Financial Health (20 points)
    if debt < 0.5:
        score += 20
    elif debt < 1:
        score += 15
    elif debt < 2:
        score += 8

    return score

def get_valuation_recommendations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol, quantity, buy_price FROM portfolio")
    rows = cursor.fetchall()
    conn.close()

    recommendations = []

    for symbol, qty, buy_price in rows:
        clean_symbol = symbol.split("-")[0]
        live_price = get_live_price(symbol)

        if not live_price:
            continue

        try:
            stock = yf.Ticker(f"{clean_symbol}.NS")
            info = stock.info

            # Fundamental data
            pe = info.get("trailingPE", 0) or 0
            pb = info.get("priceToBook", 0) or 0
            roe = info.get("returnOnEquity", 0)
            roe = roe * 100 if roe else 0

            # ROCE is not always available directly
            roce = info.get("returnOnAssets", 0)
            roce = roce * 100 if roce else 0

            debt = info.get("debtToEquity", 0) or 0

            rev_growth = info.get("revenueGrowth", 0)
            rev_growth = rev_growth * 100 if rev_growth else 0

            profit_growth = info.get("earningsGrowth", 0)
            profit_growth = profit_growth * 100 if profit_growth else 0

            eps = info.get("trailingEps", 0) or 0

            # Graham Value
            if eps > 0:
                graham_value = (22.5 * eps * 1.5) ** 0.5
            else:
                graham_value = 0

            mos = ((graham_value - live_price) / live_price) * 100 if graham_value > 0 else 0

            # Calculate 100-point score
            score = calculate_score(pe, pb, roe, roce, debt, rev_growth, profit_growth, mos)

            # Recommendation
            if score >= 80:
                recommendation = "Strong BUY"
            elif score >= 65:
                recommendation = "BUY"
            elif score >= 50:
                recommendation = "HOLD"
            elif score >= 35:
                recommendation = "REDUCE"
            else:
                recommendation = "SELL"

            recommendations.append({
                "symbol": symbol,
                "live_price": round(live_price, 2),
                "pe": round(pe, 2),
                "roe": round(roe, 2),
                "roce": round(roce, 2),
                "debt": round(debt, 2),
                "score": score,
                "recommendation": recommendation
            })

        except Exception:
            continue

    # Sort by score descending
    recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)

    return recommendations