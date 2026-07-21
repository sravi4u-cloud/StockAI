from database.db_manager import get_portfolio
from data.stock_fetcher import fetch_stock_data

# Approximate sector average P/E ratios
SECTOR_PE = {
    "Technology": 30,
    "Financial Services": 18,
    "Industrials": 28,
    "Healthcare": 35,
    "Consumer Cyclical": 32,
    "Consumer Defensive": 40,
    "Energy": 12,
    "Utilities": 20,
    "Basic Materials": 15,
    "Communication Services": 25,
    "Real Estate": 20
}

def to_float(value):
    try:
        return float(value)
    except:
        return 0.0

def sector_adjusted_fair_value():
    holdings = get_portfolio()

    if not holdings:
        print("Portfolio is empty.")
        return

    processed_symbols = set()
    results = []

    for holding in holdings:
        _, symbol, _, _, _ = holding

        if symbol in processed_symbols:
            continue

        processed_symbols.add(symbol)

        stock_data = fetch_stock_data(symbol)

        if not stock_data:
            continue

        current_price = to_float(stock_data.get("current_price", 0))
        pe_ratio = to_float(stock_data.get("pe_ratio", 0))
        sector = stock_data.get("sector", "Unknown")

        # Get sector average P/E
        sector_pe = SECTOR_PE.get(sector, 25)

        # Estimate EPS
        eps = current_price / pe_ratio if pe_ratio > 0 else 0

        # Fair value based on sector P/E
        fair_value = eps * sector_pe

        # Premium or discount
        premium_discount = ((current_price - fair_value) / fair_value) * 100 if fair_value > 0 else 0

        # Expected growth adjustment
        growth_rate = 10  # Default expected growth rate
        growth_adjusted_fair_value = fair_value * (1 + growth_rate / 100)

        results.append({
            "symbol": symbol,
            "sector": sector,
            "current_price": current_price,
            "pe_ratio": pe_ratio,
            "sector_pe": sector_pe,
            "fair_value": fair_value,
            "growth_adjusted_fair_value": growth_adjusted_fair_value,
            "premium_discount": premium_discount
        })

    # Sort by most undervalued
    results.sort(key=lambda x: x["premium_discount"])

    # ---------------- OUTPUT ----------------
    print("\n" + "=" * 100)
    print("                SECTOR-ADJUSTED FAIR VALUE ENGINE")
    print("=" * 100)

    print(f"{'Stock':<15}{'Sector':<20}{'Price':<12}{'P/E':<8}{'Sector P/E':<12}{'Fair Value':<15}{'Premium/Discount':<18}")
    print("-" * 100)

    for stock in results:
        status = "Undervalued" if stock['premium_discount'] < 0 else "Overvalued"

        print(
            f"{stock['symbol']:<15}"
            f"{stock['sector'][:18]:<20}"
            f"₹{stock['current_price']:<11.2f}"
            f"{stock['pe_ratio']:<8.2f}"
            f"{stock['sector_pe']:<12.2f}"
            f"₹{stock['fair_value']:<14.2f}"
            f"{stock['premium_discount']:<17.2f}%"
        )

    print("-" * 100)

    # Top undervalued stocks
    print("\nTOP UNDERVALUED STOCKS:")

    undervalued = [s for s in results if s['premium_discount'] < 0][:5]

    for stock in undervalued:
        print(
            f"• {stock['symbol']} — {abs(stock['premium_discount']):.2f}% below sector fair value"
        )

    print("=" * 100)