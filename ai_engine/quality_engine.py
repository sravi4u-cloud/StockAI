from database.db_manager import get_portfolio
from data.stock_fetcher import fetch_stock_data

def to_float(value):
    try:
        return float(value)
    except:
        return 0.0

def smart_quality_valuation_engine():
    holdings = get_portfolio()

    if not holdings:
        print("Portfolio is empty.")
        return

    ranked_stocks = []
    processed_symbols = set()

    for holding in holdings:
        _, symbol, _, _, _ = holding

        # Skip duplicates
        if symbol in processed_symbols:
            continue

        processed_symbols.add(symbol)

        stock_data = fetch_stock_data(symbol)

        if not stock_data:
            continue

        current_price = to_float(stock_data.get("current_price", 0))
        pe_ratio = to_float(stock_data.get("pe_ratio", 0))
        roe = to_float(stock_data.get("roe", 0)) * 100

        # Quality Score (40)
        quality_score = 40 if roe > 20 else 30 if roe > 15 else 20 if roe > 10 else 10

        # Valuation Score (30)
        if pe_ratio <= 0:
            valuation_score = 10
        elif pe_ratio < 15:
            valuation_score = 30
        elif pe_ratio < 25:
            valuation_score = 25
        elif pe_ratio < 40:
            valuation_score = 20
        else:
            valuation_score = 10

        # Growth Score (20)
        growth_score = 20 if roe > 20 else 15 if roe > 15 else 10

        # Risk Score (10)
        risk_score = 10

        final_score = min(100, quality_score + valuation_score + growth_score + risk_score)

        ranked_stocks.append({
            "symbol": symbol,
            "current_price": current_price,
            "pe_ratio": pe_ratio,
            "roe": roe,
            "score": final_score
        })

    ranked_stocks.sort(key=lambda x: x["score"], reverse=True)

    print("\n" + "=" * 75)
    print("        SMART QUALITY & VALUATION ENGINE")
    print("=" * 75)
    print(f"{'Rank':<6}{'Stock':<15}{'Price':<12}{'P/E':<10}{'ROE %':<10}{'Score':<10}")
    print("-" * 75)

    for idx, stock in enumerate(ranked_stocks, start=1):
        print(f"{idx:<6}{stock['symbol']:<15}₹{stock['current_price']:<11.2f}{stock['pe_ratio']:<10.2f}{stock['roe']:<10.2f}{stock['score']:<10}")

    print("-" * 75)
    print("\nTOP INVESTMENT OPPORTUNITIES:")

    for stock in ranked_stocks[:5]:
        print(f"• {stock['symbol']} — Score: {stock['score']}/100")

    print("=" * 75)