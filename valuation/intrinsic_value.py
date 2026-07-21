from data.stock_fetcher import fetch_stock_data

def calculate_intrinsic_value():
    symbol = input("Enter NSE stock symbol: ").upper()

    if not symbol.endswith(".NS"):
        symbol += ".NS"

    stock_data = fetch_stock_data(symbol)

    if not stock_data:
        print("Could not fetch stock data.")
        return

    current_price = stock_data["current_price"]

    print(f"\nCurrent Price of {symbol}: ₹{current_price}")

    # User inputs
    eps = float(input("Enter EPS (Earnings Per Share): ₹"))
    growth_rate = float(input("Enter expected annual growth rate (%): "))

    # Graham Formula
    intrinsic_value = eps * (8.5 + 2 * growth_rate)

    margin_of_safety = ((intrinsic_value - current_price) / intrinsic_value) * 100

    print("\n" + "=" * 50)
    print("      INTRINSIC VALUE ANALYSIS")
    print("=" * 50)
    print(f"Stock: {symbol}")
    print(f"Current Price: ₹{current_price:.2f}")
    print(f"EPS: ₹{eps:.2f}")
    print(f"Growth Rate: {growth_rate:.2f}%")
    print(f"Intrinsic Value: ₹{intrinsic_value:.2f}")
    print(f"Margin of Safety: {margin_of_safety:.2f}%")

    if current_price < intrinsic_value:
        print("Valuation: UNDERVALUED - Potential BUY opportunity")
    elif current_price > intrinsic_value:
        print("Valuation: OVERVALUED - Caution advised")
    else:
        print("Valuation: FAIRLY VALUED")

    print("=" * 50)