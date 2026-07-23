from ai_engine.earnings_forecast import ai_earnings_forecast
from sentiment.news_sentiment import analyze_news_sentiment
from fundamental.financial_analysis import financial_statement_analysis
from screener.realtime_screener import run_realtime_screener
from portfolio.action_plan import personalized_action_plan
from ai_engine.sector_adjusted_engine import sector_adjusted_fair_value
from ai_engine.quality_engine import smart_quality_valuation_engine
from ai_engine.recommendation_engine import calculate_recommendation
from database.init_db import init_database
from portfolio.portfolio_manager import (
    add_holding,
    view_portfolio,
    remove_holding
)
from watchlist.watchlist_manager import (
    
    add_to_watchlist,
    get_watchlist,
    remove_from_watchlist,
    
)
from portfolio.analytics import portfolio_dashboard
from portfolio.excel_import import import_portfolio_from_excel
from valuation.intrinsic_value import calculate_intrinsic_value
from valuation.dcf_engine import calculate_dcf

def portfolio_menu():
    while True:
        print("\n=== PORTFOLIO MENU ===")
        print("1. Add Holding")
        print("2. View Portfolio")
        print("3. Delete Holding")
        print("4. Portfolio Analytics Dashboard")
        print("5. Import Portfolio from Excel")
        print("6. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            add_holding()
        elif choice == "2":
            view_portfolio()
        elif choice == "3":
            remove_holding()
        elif choice == "4":
            portfolio_dashboard()
        elif choice == "5":
            file_path = input("Enter Excel file path: ")
            import_portfolio_from_excel(file_path)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

def watchlist_menu():
    while True:
        print("\n=== WATCHLIST MENU ===")
        print("1. add_to_watchlist")
        print("2. get_watchlist")
        print("3. remove_from_watchlist")
        print("4. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            add_to_watchlist()
        elif choice == "2":
            get_watchlist()
        elif choice == "3":
            remove_from_watchlist()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")

def valuation_menu():
    while True:
        print("\n=== VALUATION MENU ===")
        print("1. Intrinsic Value Calculator")
        print("2. DCF Valuation Engine")
        print("3. Back to Main Menu")

        choice = input("Enter choice: ")

        if choice == "1":
            calculate_intrinsic_value()
        elif choice == "2":
            calculate_dcf()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

def main():
    init_database()

    while True:
        print("\n" + "=" * 50)
        print("           AI STOCK ANALYZER")
        print("=" * 50)
        print("1. Portfolio")
        print("2. Watchlist")
        print("3. Valuation Engine")
        print("4. AI BUY/HOLD/SELL Recommendation")
        print("5. Smart Quality & Valuation Engine")
        print("6. Sector-Adjusted Fair Value Engine")
        print("7. Personalized Portfolio Action Plan")
        print("8. Real-Time Stock Screener & Alert Engine")
        print("9. Financial Statement Analysis Engine")
        print("10. News & Sentiment Analysis Engine")
        print("11. AI Earnings Forecast & Multibagger Prediction")
        print("12. Exit")

        choice = input("\nEnter choice: ")

        if choice == "1":
            portfolio_menu()
        elif choice == "2":
            watchlist_menu()
        elif choice == "3":
            valuation_menu()
        elif choice == "4":
            calculate_recommendation()
        elif choice == "5":
            smart_quality_valuation_engine()
        elif choice == "6":
            sector_adjusted_fair_value()
        elif choice == "7":
            personalized_action_plan()
        elif choice == "8":
            run_realtime_screener()
        elif choice == "9":
            financial_statement_analysis()
        elif choice == "10":
            analyze_news_sentiment()
        elif choice == "11":
            ai_earnings_forecast()
        elif choice == "12":
            print("\nThank you for using AI Stock Analyzer!")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-12.")

if __name__ == "__main__":
    main()