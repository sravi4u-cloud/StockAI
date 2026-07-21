from data.stock_fetcher import fetch_stock_data

def calculate_dcf():
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
    fcf = float(input("Enter current Free Cash Flow (in Crores): ₹"))
    growth_rate = float(input("Enter expected FCF growth rate (%): ")) / 100
    discount_rate = float(input("Enter discount rate (%): ")) / 100
    terminal_growth = float(input("Enter terminal growth rate (%): ")) / 100
    shares_outstanding = float(input("Enter shares outstanding (in Crores): "))

    # DCF Calculation
    years = 5
    present_value = 0
    projected_fcf = fcf

    for year in range(1, years + 1):
        projected_fcf *= (1 + growth_rate)
        discounted_fcf = projected_fcf / ((1 + discount_rate) ** year)
        present_value += discounted_fcf

    # Terminal Value
    terminal_value = (projected_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    discounted_terminal = terminal_value / ((1 + discount_rate) ** years)

    total_value = present_value + discounted_terminal
    intrinsic_value_per_share = total_value / shares_outstanding

    margin_of_safety = ((intrinsic_value_per_share - current_price) / intrinsic_value_per_share) * 100

    print("\n" + "=" * 50)
    print("           DCF VALUATION REPORT")
    print("=" * 50)
    print(f"Stock: {symbol}")
    print(f"Current Price: ₹{current_price:.2f}")
    print(f"Projected Enterprise Value: ₹{total_value:,.2f} Cr")
    print(f"Intrinsic Value per Share: ₹{intrinsic_value_per_share:.2f}")
    print(f"Margin of Safety: {margin_of_safety:.2f}%")

    if current_price < intrinsic_value_per_share:
        print("Valuation: UNDERVALUED - Potential BUY opportunity")
    elif current_price > intrinsic_value_per_share:
        print("Valuation: OVERVALUED - Caution advised")
    else:
        print("Valuation: FAIRLY VALUED")

    print("=" * 50)