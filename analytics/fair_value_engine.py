import yfinance as yf
from database.database import get_connection
from data.downloader import get_live_price

# Sector-wise fair P/E benchmarks
SECTOR_PE = {
    "Banking": 15,
    "IT": 25,
    "Consumer": 35,
    "Defence": 30,
    "Insurance": 35,
    "Financial Services": 25,
    "Auto": 20,
    "Chemicals": 25,
    "Others": 20
}

# Map your portfolio stocks to sectors
SECTOR_MAP = {
    "SBIN": "Banking",
    "HDFCBANK": "Banking",
    "AUBANK": "Banking",
    "UJJIVANSFB": "Banking",
    "INFY": "IT",
    "WIPRO": "IT",
    "HAL": "Defence",
    "POLYCAB": "Others",
    "CAMS": "Financial Services",
    "ICICIGI": "Insurance",
    "M&M": "Auto",
    "VEDL": "Others"
}

def get_fair_value_recommendations():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT symbol FROM portfolio")
    rows = cursor.fetchall()
    conn.close()

    recommendations = []

    for row in rows:
        symbol = row[0]
        clean_symbol = symbol.split("-")[0]

        live_price = get_live_price(symbol)
        if not live_price:
            continue

        try:
            stock = yf.Ticker(f"{clean_symbol}.NS")
            info = stock.info

            eps = info.get("trailingEps", 0) or 0
            pe = info.get("trailingPE", 0) or 0

            sector = SECTOR_MAP.get(clean_symbol, "Others")
            fair_pe = SECTOR_PE.get(sector, 20)

            # Calculate target price
            target_price = eps * fair_pe if eps > 0 else live_price

            upside = ((target_price - live_price) / live_price) * 100

            # Confidence score
            confidence = 50

            roe = info.get("returnOnEquity", 0)
            roe = roe * 100 if roe else 0

            debt = info.get("debtToEquity", 0) or 0

            if roe > 20:
                confidence += 20
            elif roe > 15:
                confidence += 10

            if debt < 0.5:
                confidence += 15
            elif debt < 1:
                confidence += 8

            if pe > 0 and pe < fair_pe:
                confidence += 15

            confidence = min(confidence, 100)

            # Recommendation
            if upside > 25 and confidence >= 70:
                recommendation = "STRONG BUY"
            elif upside > 10 and confidence >= 60:
                recommendation = "BUY"
            elif upside > -10:
                recommendation = "HOLD"
            elif upside > -25:
                recommendation = "REDUCE"
            else:
                recommendation = "SELL"

            recommendations.append({
                "symbol": symbol,
                "sector": sector,
                "live_price": round(live_price, 2),
                "target_price": round(target_price, 2),
                "upside": round(upside, 2),
                "confidence": confidence,
                "recommendation": recommendation
            })

        except Exception:
            continue

    # Sort by upside potential
    recommendations = sorted(recommendations, key=lambda x: x["upside"], reverse=True)

    return recommendations