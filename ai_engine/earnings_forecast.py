import yfinance as yf

def ai_earnings_forecast():
    symbol = input("Enter NSE stock symbol: ").upper()

    if not symbol.endswith(".NS"):
        symbol += ".NS"

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        current_price = info.get("currentPrice", 0)
        current_eps = info.get("trailingEps", 0)
        current_pe = info.get("trailingPE", 0)
        roe = (info.get("returnOnEquity", 0) or 0) * 100

        if current_eps == 0:
            print("EPS data not available for this stock.")
            return

        print("\n" + "=" * 80)
        print(f"      AI EARNINGS FORECAST & MULTIBAGGER ANALYSIS - {symbol}")
        print("=" * 80)

        print(f"Current Price: ₹{current_price:.2f}")
        print(f"Current EPS: ₹{current_eps:.2f}")
        print(f"Current P/E: {current_pe:.2f}")
        print(f"ROE: {roe:.2f}%")

        # User assumptions
        growth_rate = float(input("\nExpected EPS growth rate (%): "))
        future_pe = float(input("Expected future P/E multiple: "))
        years = int(input("Forecast period (years): "))

        # Forecast EPS
        future_eps = current_eps * ((1 + growth_rate / 100) ** years)

        # Future fair value
        future_price = future_eps * future_pe

        # Potential return
        potential_return = ((future_price - current_price) / current_price) * 100

        # CAGR
        cagr = ((future_price / current_price) ** (1 / years) - 1) * 100

        # Multibagger category
        multiple = future_price / current_price

        if multiple >= 10:
            category = "10X Multibagger"
        elif multiple >= 5:
            category = "5X Multibagger"
        elif multiple >= 3:
            category = "3X Multibagger"
        elif multiple >= 2:
            category = "2X Multibagger"
        else:
            category = "No Multibagger"

        # AI confidence score
        confidence = 50

        if roe > 20:
            confidence += 20
        elif roe > 15:
            confidence += 10

        if growth_rate > 15:
            confidence += 15
        elif growth_rate > 10:
            confidence += 10

        if current_pe < future_pe:
            confidence += 10

        confidence = min(confidence, 100)

        # Output
        print("\n" + "-" * 80)
        print("FORECAST RESULTS")
        print("-" * 80)
        print(f"Forecast Period: {years} years")
        print(f"Expected EPS Growth: {growth_rate:.2f}% CAGR")
        print(f"Future EPS: ₹{future_eps:.2f}")
        print(f"Future P/E Multiple: {future_pe:.2f}")
        print(f"Future Fair Value: ₹{future_price:.2f}")

        print("\n" + "-" * 80)
        print("RETURN ANALYSIS")
        print("-" * 80)
        print(f"Potential Return: {potential_return:.2f}%")
        print(f"Expected CAGR: {cagr:.2f}% per year")
        print(f"Price Multiple: {multiple:.2f}x")

        print("\n" + "-" * 80)
        print("MULTIBAGGER PREDICTION")
        print("-" * 80)
        print(f"Category: {category}")
        print(f"AI Confidence Score: {confidence}/100")

        # Investment signal
        if multiple >= 3 and confidence >= 70:
            signal = "HIGH MULTIBAGGER POTENTIAL"
        elif multiple >= 2 and confidence >= 60:
            signal = "GOOD LONG-TERM OPPORTUNITY"
        else:
            signal = "MODERATE POTENTIAL"

        print(f"Investment Signal: {signal}")

        print("\n" + "=" * 80)

    except Exception as e:
        print(f"Error in forecasting: {e}")