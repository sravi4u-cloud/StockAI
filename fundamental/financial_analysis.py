import yfinance as yf
import pandas as pd

def financial_statement_analysis():
    symbol = input("Enter NSE stock symbol: ").upper()

    if not symbol.endswith(".NS"):
        symbol += ".NS"

    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Fetch financial statements
        income_stmt = stock.financials
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cashflow

        print("\n" + "=" * 80)
        print(f"      FINANCIAL STATEMENT ANALYSIS - {symbol}")
        print("=" * 80)

        # Company info
        print(f"Company: {info.get('longName', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")

        # ---------------- REVENUE ANALYSIS ----------------
        print("\n" + "-" * 80)
        print("REVENUE ANALYSIS")
        print("-" * 80)

        if "Total Revenue" in income_stmt.index:
            revenues = income_stmt.loc["Total Revenue"]

            for year, value in revenues.items():
                print(f"{year.year}: ₹{value/1e7:,.2f} Cr")

            # Revenue growth
            if len(revenues) >= 2:
                latest = revenues.iloc[0]
                previous = revenues.iloc[1]
                growth = ((latest - previous) / previous) * 100
                print(f"Revenue Growth: {growth:.2f}%")

        # ---------------- PROFIT ANALYSIS ----------------
        print("\n" + "-" * 80)
        print("NET PROFIT ANALYSIS")
        print("-" * 80)

        if "Net Income" in income_stmt.index:
            profits = income_stmt.loc["Net Income"]

            for year, value in profits.items():
                print(f"{year.year}: ₹{value/1e7:,.2f} Cr")

            if len(profits) >= 2:
                latest = profits.iloc[0]
                previous = profits.iloc[1]
                profit_growth = ((latest - previous) / previous) * 100
                print(f"Net Profit Growth: {profit_growth:.2f}%")

        # ---------------- CASH FLOW ANALYSIS ----------------
        print("\n" + "-" * 80)
        print("CASH FLOW ANALYSIS")
        print("-" * 80)

        if "Operating Cash Flow" in cash_flow.index:
            ocf = cash_flow.loc["Operating Cash Flow"]

            for year, value in ocf.items():
                print(f"{year.year}: ₹{value/1e7:,.2f} Cr")

        # ---------------- DEBT ANALYSIS ----------------
        print("\n" + "-" * 80)
        print("DEBT ANALYSIS")
        print("-" * 80)

        total_debt = balance_sheet.loc["Total Debt"].iloc[0] if "Total Debt" in balance_sheet.index else 0
        total_equity = balance_sheet.loc["Stockholders Equity"].iloc[0] if "Stockholders Equity" in balance_sheet.index else 0

        debt_equity = total_debt / total_equity if total_equity > 0 else 0

        print(f"Total Debt: ₹{total_debt/1e7:,.2f} Cr")
        print(f"Total Equity: ₹{total_equity/1e7:,.2f} Cr")
        print(f"Debt/Equity Ratio: {debt_equity:.2f}")

        # ---------------- PROFITABILITY RATIOS ----------------
        print("\n" + "-" * 80)
        print("PROFITABILITY RATIOS")
        print("-" * 80)

        roe = info.get("returnOnEquity", 0) or 0
        operating_margin = info.get("operatingMargins", 0) or 0
        profit_margin = info.get("profitMargins", 0) or 0

        print(f"ROE: {roe*100:.2f}%")
        print(f"Operating Margin: {operating_margin*100:.2f}%")
        print(f"Net Profit Margin: {profit_margin*100:.2f}%")

        # ---------------- AI FUNDAMENTAL SCORE ----------------
        score = 0

        if roe > 0.20:
            score += 30
        elif roe > 0.15:
            score += 20
        else:
            score += 10

        if debt_equity < 0.3:
            score += 25
        elif debt_equity < 0.5:
            score += 15
        else:
            score += 5

        if operating_margin > 0.20:
            score += 25
        elif operating_margin > 0.10:
            score += 15
        else:
            score += 5

        if profit_margin > 0.15:
            score += 20
        elif profit_margin > 0.08:
            score += 10
        else:
            score += 5

        print("\n" + "-" * 80)
        print("AI FUNDAMENTAL SCORE")
        print("-" * 80)
        print(f"Fundamental Score: {score}/100")

        if score >= 75:
            recommendation = "STRONG BUY"
        elif score >= 60:
            recommendation = "BUY"
        elif score >= 45:
            recommendation = "HOLD"
        else:
            recommendation = "AVOID"

        print(f"Fundamental Recommendation: {recommendation}")

        print("\n" + "=" * 80)

    except Exception as e:
        print(f"Error analyzing financial statements: {e}")