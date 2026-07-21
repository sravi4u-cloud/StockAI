from database.db_manager import get_portfolio
from data.stock_fetcher import fetch_stock_data
from datetime import datetime
from collections import defaultdict

def calculate_cagr(initial_value, final_value, years):
    if initial_value <= 0 or years <= 0:
        return 0
    return ((final_value / initial_value) ** (1 / years) - 1) * 100

def portfolio_dashboard():
    holdings = get_portfolio()

    if not holdings:
        print("Portfolio is empty.")
        return

    total_invested = 0
    total_current = 0
    sector_allocation = defaultdict(float)
    stock_performance = []

    for holding in holdings:
        holding_id, symbol, quantity, buy_price, buy_date = holding

        stock_data = fetch_stock_data(symbol)

        if not stock_data:
            continue

        current_price = stock_data["current_price"]
        sector = stock_data["sector"]

        invested = quantity * buy_price
        current_value = quantity * current_price
        pnl = current_value - invested
        pnl_percent = (pnl / invested) * 100 if invested > 0 else 0

        total_invested += invested
        total_current += current_value

        sector_allocation[sector] += current_value

        stock_performance.append({
            "symbol": symbol,
            "pnl": pnl,
            "pnl_percent": pnl_percent
        })

    # Calculate CAGR
    first_buy_date = min(
        [datetime.strptime(h[4], "%Y-%m-%d") for h in holdings]
    )
    years = (datetime.now() - first_buy_date).days / 365.25
    cagr = calculate_cagr(total_invested, total_current, years)

    # Diversification Score
    max_sector = max(sector_allocation.values())
    concentration = (max_sector / total_current) * 100
    diversification_score = max(0, 100 - concentration)

    # Top Gainers and Losers
    stock_performance.sort(key=lambda x: x["pnl_percent"], reverse=True)

    top_gainers = stock_performance[:3]
    top_losers = stock_performance[-3:]

    # Print Dashboard
    print("\n" + "=" * 50)
    print("      PORTFOLIO ANALYTICS DASHBOARD")
    print("=" * 50)

    print(f"\nTotal Invested: ₹{total_invested:,.2f}")
    print(f"Current Value: ₹{total_current:,.2f}")

    total_pnl = total_current - total_invested
    total_pnl_percent = (total_pnl / total_invested) * 100

    print(f"Total P&L: ₹{total_pnl:,.2f} ({total_pnl_percent:.2f}%)")
    print(f"Portfolio CAGR: {cagr:.2f}%")
    print(f"Diversification Score: {diversification_score:.2f}/100")

    # Sector Allocation
    print("\n" + "-" * 50)
    print("SECTOR ALLOCATION")
    print("-" * 50)

    for sector, value in sector_allocation.items():
        percentage = (value / total_current) * 100
        print(f"{sector}: ₹{value:,.2f} ({percentage:.2f}%)")

    # Top Gainers
    print("\n" + "-" * 50)
    print("TOP GAINERS")
    print("-" * 50)

    for stock in top_gainers:
        print(f"{stock['symbol']}: {stock['pnl_percent']:.2f}%")

    # Top Losers
    print("\n" + "-" * 50)
    print("TOP LOSERS")
    print("-" * 50)

    for stock in top_losers:
        print(f"{stock['symbol']}: {stock['pnl_percent']:.2f}%")

    print("\n" + "=" * 50)