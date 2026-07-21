from database.db_manager import get_portfolio
from data.stock_fetcher import fetch_stock_data
from collections import defaultdict

def to_float(value):
    try:
        return float(value)
    except:
        return 0.0

def personalized_action_plan():
    holdings = get_portfolio()

    if not holdings:
        print("Portfolio is empty.")
        return

    sector_values = defaultdict(float)
    stock_actions = []
    total_portfolio_value = 0

    # Calculate portfolio values
    for holding in holdings:
        _, symbol, quantity, buy_price, _ = holding

        stock_data = fetch_stock_data(symbol)

        if not stock_data:
            continue

        current_price = to_float(stock_data.get("current_price", 0))
        sector = stock_data.get("sector", "Unknown")
        pe_ratio = to_float(stock_data.get("pe_ratio", 0))
        roe = to_float(stock_data.get("roe", 0)) * 100

        current_value = quantity * current_price
        total_portfolio_value += current_value
        sector_values[sector] += current_value

        # Simple action logic
        if roe > 20 and pe_ratio < 25:
            action = "BUY"
        elif roe > 15 and pe_ratio < 40:
            action = "HOLD"
        elif pe_ratio > 60:
            action = "REDUCE"
        else:
            action = "HOLD"

        stock_actions.append({
            "symbol": symbol,
            "sector": sector,
            "current_value": current_value,
            "pe_ratio": pe_ratio,
            "roe": roe,
            "action": action
        })

    # Determine sector concentration
    sector_actions = []

    for sector, value in sector_values.items():
        allocation = (value / total_portfolio_value) * 100

        if allocation > 35:
            sector_actions.append((sector, allocation, "OVERWEIGHT - Reduce exposure"))
        elif allocation < 10:
            sector_actions.append((sector, allocation, "UNDERWEIGHT - Consider adding"))
        else:
            sector_actions.append((sector, allocation, "Balanced"))

    # ---------------- OUTPUT ----------------
    print("\n" + "=" * 90)
    print("              PERSONALIZED PORTFOLIO ACTION PLAN")
    print("=" * 90)

    print(f"\nTotal Portfolio Value: ₹{total_portfolio_value:,.2f}")

    # Sector allocation analysis
    print("\n" + "-" * 90)
    print("SECTOR ALLOCATION ANALYSIS")
    print("-" * 90)

    for sector, allocation, status in sorted(sector_actions, key=lambda x: x[1], reverse=True):
        print(f"{sector:<25} {allocation:6.2f}%   {status}")

    # Stock recommendations
    print("\n" + "-" * 90)
    print("STOCK ACTION RECOMMENDATIONS")
    print("-" * 90)

    print(f"{'Stock':<15}{'Sector':<20}{'P/E':<10}{'ROE %':<10}{'Action':<15}")
    print("-" * 90)

    for stock in stock_actions:
        print(
            f"{stock['symbol']:<15}"
            f"{stock['sector'][:18]:<20}"
            f"{stock['pe_ratio']:<10.2f}"
            f"{stock['roe']:<10.2f}"
            f"{stock['action']:<15}"
        )

    # Summary actions
    buy_count = sum(1 for s in stock_actions if s["action"] == "BUY")
    hold_count = sum(1 for s in stock_actions if s["action"] == "HOLD")
    reduce_count = sum(1 for s in stock_actions if s["action"] == "REDUCE")

    print("\n" + "-" * 90)
    print("ACTION PLAN SUMMARY")
    print("-" * 90)
    print(f"BUY Opportunities   : {buy_count}")
    print(f"HOLD Positions      : {hold_count}")
    print(f"REDUCE Positions    : {reduce_count}")

    print("\nPRIORITY ACTIONS:")

    # Show top BUY opportunities
    buy_stocks = [s for s in stock_actions if s["action"] == "BUY"][:5]

    for stock in buy_stocks:
        print(f"• BUY / ACCUMULATE: {stock['symbol']} (ROE {stock['roe']:.1f}%, P/E {stock['pe_ratio']:.1f})")

    # Show top REDUCE opportunities
    reduce_stocks = [s for s in stock_actions if s["action"] == "REDUCE"][:5]

    for stock in reduce_stocks:
        print(f"• REDUCE: {stock['symbol']} (High P/E {stock['pe_ratio']:.1f})")

    print("=" * 90)