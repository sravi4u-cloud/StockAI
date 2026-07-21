from data.stock_fetcher import fetch_stock_data

def calculate_recommendation():
    symbol = input("Enter NSE stock symbol: ").upper()

    if not symbol.endswith(".NS"):
        symbol += ".NS"

    stock_data = fetch_stock_data(symbol)

    if not stock_data:
        print("Could not fetch stock data.")
        return

    current_price = stock_data["current_price"]
    pe_ratio = stock_data["pe_ratio"]
    roe = stock_data["roe"]

    # User inputs for analysis
    growth_rate = float(input("Enter expected revenue/profit growth rate (%): "))
    debt_equity = float(input("Enter Debt/Equity ratio: "))
    intrinsic_value = float(input("Enter calculated intrinsic value: ₹"))

    # ---------------- SCORING MODEL ----------------

    # Valuation Score (30%)
    if current_price < intrinsic_value * 0.8:
        valuation_score = 100
    elif current_price < intrinsic_value:
        valuation_score = 75
    elif current_price < intrinsic_value * 1.2:
        valuation_score = 50
    else:
        valuation_score = 25

    # Growth Score (25%)
    if growth_rate > 20:
        growth_score = 100
    elif growth_rate > 15:
        growth_score = 80
    elif growth_rate > 10:
        growth_score = 60
    else:
        growth_score = 40

    # Quality Score (25%)
    if roe and roe > 0.20:
        quality_score = 100
    elif roe and roe > 0.15:
        quality_score = 80
    elif roe and roe > 0.10:
        quality_score = 60
    else:
        quality_score = 40

    # Risk Score (20%)
    if debt_equity < 0.3:
        risk_score = 100
    elif debt_equity < 0.5:
        risk_score = 80
    elif debt_equity < 1:
        risk_score = 60
    else:
        risk_score = 40

    # Final Weighted Score
    final_score = (
        valuation_score * 0.30 +
        growth_score * 0.25 +
        quality_score * 0.25 +
        risk_score * 0.20
    )

    # Recommendation Logic
    if final_score >= 80:
        recommendation = "BUY"
    elif final_score >= 60:
        recommendation = "HOLD"
    else:
        recommendation = "SELL"

    # Margin of Safety
    margin_of_safety = ((intrinsic_value - current_price) / intrinsic_value) * 100

    # ---------------- OUTPUT ----------------

    print("\n" + "=" * 60)
    print("        AI BUY / HOLD / SELL RECOMMENDATION")
    print("=" * 60)
    print(f"Stock: {symbol}")
    print(f"Current Price: ₹{current_price:.2f}")
    print(f"Intrinsic Value: ₹{intrinsic_value:.2f}")
    print(f"Margin of Safety: {margin_of_safety:.2f}%")
    print("-" * 60)
    print(f"Valuation Score: {valuation_score}/100")
    print(f"Growth Score: {growth_score}/100")
    print(f"Quality Score: {quality_score}/100")
    print(f"Risk Score: {risk_score}/100")
    print("-" * 60)
    print(f"FINAL SCORE: {final_score:.2f}/100")
    print(f"RECOMMENDATION: {recommendation}")
    print("-" * 60)

    # Reasoning
    print("AI Reasoning:")

    if valuation_score >= 75:
        print("• The stock appears attractively valued compared to its intrinsic value.")
    else:
        print("• The stock may be trading at a premium valuation.")

    if growth_score >= 80:
        print("• Strong growth expectations support future earnings expansion.")
    else:
        print("• Growth expectations are moderate.")

    if quality_score >= 80:
        print("• High ROE indicates strong business quality and capital efficiency.")
    else:
        print("• Business quality is average based on ROE.")

    if risk_score >= 80:
        print("• Low debt levels reduce financial risk.")
    else:
        print("• Higher debt levels increase financial risk.")

    print("=" * 60)