import yfinance as yf
from datetime import datetime

from alerts.telegram_alert import send_telegram_alert

# Sample NSE stocks for screening
NSE_STOCKS = [
    "HAL.NS", "SIEMENS.NS", "BDL.NS", "SBIN.NS", "INFY.NS",
    "TCS.NS", "POLYCAB.NS", "ICICIBANK.NS", "HDFCBANK.NS",
    "RELIANCE.NS", "LT.NS", "TATAMOTORS.NS", "BAJFINANCE.NS",
    "APOLLOHOSP.NS", "MAXHEALTH.NS"
]

def calculate_score(pe_ratio, roe):
    """Simple quality + valuation scoring model"""

    valuation_score = 0
    if pe_ratio > 0 and pe_ratio < 15:
        valuation_score = 40
    elif pe_ratio < 25:
        valuation_score = 30
    elif pe_ratio < 40:
        valuation_score = 20
    else:
        valuation_score = 10

    quality_score = 0
    if roe > 20:
        quality_score = 60
    elif roe > 15:
        quality_score = 45
    elif roe > 10:
        quality_score = 30
    else:
        quality_score = 15

    return valuation_score + quality_score

def run_realtime_screener():
    print("\nScanning NSE stocks in real-time...")
    print("Please wait, this may take a few seconds.\n")

    screened_stocks = []

    for symbol in NSE_STOCKS:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            current_price = info.get("currentPrice", 0)
            pe_ratio = info.get("trailingPE", 0) or 0
            roe = info.get("returnOnEquity", 0) or 0

            # Convert ROE to percentage
            roe_percent = roe * 100 if roe else 0

            score = calculate_score(pe_ratio, roe_percent)

            screened_stocks.append({
                "symbol": symbol,
                "price": current_price,
                "pe": pe_ratio,
                "roe": roe_percent,
                "score": score
            })

        except Exception:
            continue

    # Sort by highest score
    screened_stocks.sort(key=lambda x: x["score"], reverse=True)

    # Display results
    print("=" * 75)
    print("           REAL-TIME STOCK SCREENER RESULTS")
    print("=" * 75)
    print(f"{'Rank':<6}{'Stock':<15}{'Price':<12}{'P/E':<10}{'ROE %':<10}{'Score':<10}")
    print("-" * 75)

    for idx, stock in enumerate(screened_stocks[:10], start=1):
        print(
            f"{idx:<6}{stock['symbol']:<15}"
            f"₹{stock['price']:<11.2f}"
            f"{stock['pe']:<10.2f}"
            f"{stock['roe']:<10.2f}"
            f"{stock['score']:<10}"
        )

    print("-" * 75)
    print("\nTOP BUY OPPORTUNITIES TODAY:")

    # Prepare Telegram message
    message = "📈 StockAI Top BUY Opportunities Today:\n\n"

    for stock in screened_stocks[:3]:
        message += (
            f"• {stock['symbol']}\n"
            f"  Score: {stock['score']}/100\n"
            f"  Price: ₹{stock['price']:.2f}\n"
            f"  P/E: {stock['pe']:.1f} | ROE: {stock['roe']:.1f}%\n\n"
        )

    # Send Telegram alert
    send_telegram_alert(message)

    for stock in screened_stocks[:5]:
        print(
            f"• {stock['symbol']} — Score: {stock['score']}/100 | "
            f"P/E: {stock['pe']:.1f} | ROE: {stock['roe']:.1f}%"
        )

    print("\nScreen completed at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 75)

    return screened_stocks