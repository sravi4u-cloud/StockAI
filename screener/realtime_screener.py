import yfinance as yf
from datetime import datetime

from alerts.telegram_alert import send_telegram_alert
from ai_engine.valuation_engine import calculate_fair_value
from ai_engine.recommendation_engine import calculate_recommendation
from database.db_manager import save_screener_result

# Sample NSE stocks for screening
NSE_STOCKS = [
    # Banking
    "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "AXISBANK.NS",
    "KOTAKBANK.NS", "INDUSINDBK.NS",

    # IT
    "TCS.NS", "INFY.NS", "WIPRO.NS", "HCLTECH.NS",
    "TECHM.NS",

    # Auto
    "MARUTI.NS", "M&M.NS", "TATAMTRDVR.NS", "BAJAJ-AUTO.NS",
    "EICHERMOT.NS",

    # Capital Goods
    "LT.NS", "SIEMENS.NS", "HAL.NS", "BDL.NS",
    "BEL.NS", "ABB.NS",

    # Consumer
    "HINDUNILVR.NS", "ITC.NS", "NESTLEIND.NS", "BRITANNIA.NS",

    # Pharma & Healthcare
    "SUNPHARMA.NS", "CIPLA.NS", "DIVISLAB.NS",
    "APOLLOHOSP.NS", "MAXHEALTH.NS",

    # Energy & Materials
    "RELIANCE.NS", "ONGC.NS", "COALINDIA.NS", "NTPC.NS",
    "POWERGRID.NS", "TATASTEEL.NS", "JSWSTEEL.NS",

    # High growth
    "POLYCAB.NS", "BAJFINANCE.NS", "PIDILITIND.NS",
    "DMART.NS", "TRENT.NS"
]

def calculate_score(pe_ratio, roe, roce, revenue_growth, debt_equity, margin, upside=0):
    """
    Advanced AI Stock Intelligence Score (0-100)
    """

    score = 0

    # Valuation (20)
    if 0 < pe_ratio < 15:
        score += 20
    elif pe_ratio < 25:
        score += 15
    elif pe_ratio < 40:
        score += 8

    # ROE (20)
    if roe >= 25:
        score += 20
    elif roe >= 15:
        score += 15
    elif roe >= 10:
        score += 8

    # ROCE (20)
    if roce >= 25:
        score += 20
    elif roce >= 15:
        score += 15
    elif roce >= 10:
        score += 8

    # Revenue Growth (15)
    if revenue_growth >= 20:
        score += 15
    elif revenue_growth >= 10:
        score += 10
    elif revenue_growth >= 5:
        score += 5

    # Debt to Equity (10)
    if debt_equity <= 0.3:
        score += 10
    elif debt_equity <= 0.7:
        score += 6

    # Profit Margin (10)
    if margin >= 20:
        score += 10
    elif margin >= 10:
        score += 6

    # Fair Value Upside (5)
    if upside >= 30:
        score += 5
    elif upside >= 15:
        score += 3

    return score
def investment_action(score, upside):
    if score >= 70 and upside >= 20:
        return "BUY"
    elif score >= 45:
        return "HOLD"
    else:
        return "AVOID"

def run_realtime_screener():
    print("\nScanning NSE stocks in real-time...")
    print("Please wait, this may take a few seconds.\n")

    screened_stocks = []

    for symbol in NSE_STOCKS:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            current_price = info.get("currentPrice", 0) or 0
            pe_ratio = info.get("trailingPE", 0) or 0
            roe = info.get("returnOnEquity", 0) or 0

            # Convert ROE to percentage
            roe_percent = roe * 100 if roe else 0

            # New Phase 4B metrics
            roce = info.get("returnOnAssets", 0) or 0
            roce_percent = roce * 100 if roce else 0

            revenue_growth = info.get("revenueGrowth", 0) or 0
            revenue_growth_percent = revenue_growth * 100 if revenue_growth else 0

            debt_equity = info.get("debtToEquity", 0) or 0
            debt_equity = debt_equity / 100 if debt_equity else 0

            margin = info.get("profitMargins", 0) or 0
            margin_percent = margin * 100 if margin else 0

            eps = info.get("trailingEps", 0) or 0
            growth = info.get("earningsGrowth", 0) or 0

            stock_data = {
                "price": current_price,
                "eps": eps,
                "growth": growth * 100,
                "roe": roe_percent,
                "debt": debt_equity,
                "margin": margin_percent
            }

            fair_value = calculate_fair_value(stock_data)

            if fair_value and current_price:
                upside = ((fair_value - current_price) / current_price) * 100
            else:
                upside = 0

            score = calculate_score(
                pe_ratio,
                roe_percent,
                roce_percent,
                revenue_growth_percent,
                debt_equity,
                margin_percent,
                upside
            )

            action = investment_action(score, upside)


            screened_stocks.append({
                "symbol": symbol,
                "price": current_price,
                "pe": pe_ratio,
                "roe": roe_percent,
                "roce": roce_percent,
                "growth": revenue_growth_percent,
                "debt": debt_equity,
                "margin": margin_percent,
                "fair_value": fair_value,
                "upside": upside,
                "score": score,
                "action": action
            })
            # Save screening result to SQLite
            try:
                save_screener_result({
                    "symbol": symbol,
                    "price": current_price,
                    "pe": pe_ratio,
                    "roe": roe_percent,
                    "score": score
                })
            except Exception:
                # If DB save fails, continue without stopping the screener
                pass

        except Exception as e:
            print(f"Skipping {symbol}: {e}")
            continue

    # Sort by highest score
    screened_stocks.sort(key=lambda x: x["score"], reverse=True)

    # Display results
    print("=" * 95)
    print("                 AI STOCK INTELLIGENCE SCANNER")
    print("=" * 95)

    print(
        f"{'Rank':<6}"
        f"{'Stock':<15}"
        f"{'Price':<12}"
        f"{'Fair Value':<12}"
        f"{'Upside':<10}"
        f"{'Score':<8}"
        f"{'Action':<10}"
    )

    print("-" * 95)

    print("\nTOP 20 AI BUY OPPORTUNITIES")
    print("-" * 95)

    top_opportunities = [
        s for s in screened_stocks
        if s["action"] == "BUY"
    ][:20]

    for idx, stock in enumerate(top_opportunities, start=1):
        print(
            f"{idx:<6}"
            f"{stock['symbol']:<15}"
            f"₹{stock['price']:<11.2f}"
            f"₹{stock['fair_value']:<11.2f}"
            f"{stock['upside']:.1f}%{'':<5}"
            f"{stock['score']:<8}"
            f"{stock['action']:<10}"
        )

    return screened_stocks
