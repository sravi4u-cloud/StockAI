import streamlit as st
import pandas as pd

# Import authentication
from auth.auth_manager import create_user, verify_user

# Import portfolio modules
from portfolio.portfolio_manager import add_holding, get_portfolio, delete_holding
from portfolio.excel_import import import_portfolio_from_excel

# Import watchlist modules
from watchlist.watchlist_manager import add_to_watchlist, get_watchlist, remove_from_watchlist

# Import valuation modules
from valuation.intrinsic_value import calculate_intrinsic_value
from valuation.dcf_engine import calculate_dcf

# Import AI modules
from ai_engine.recommendation_engine import calculate_recommendation
from ai_engine.quality_engine import smart_quality_valuation_engine
from ai_engine.sector_adjusted_engine import sector_adjusted_fair_value
from ai_engine.earnings_forecast import ai_earnings_forecast

# Import analytics modules
from portfolio.analytics import portfolio_dashboard
from portfolio.action_plan import personalized_action_plan

# Import screener and analysis modules
from screener.realtime_screener import run_realtime_screener
from fundamental.financial_analysis import financial_statement_analysis
from sentiment.news_sentiment import analyze_news_sentiment

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StockAI Professional Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- LOGIN SYSTEM ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 StockAI Login")

    menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")

    elif menu == "Register":
        new_username = st.text_input("Choose Username")
        new_password = st.text_input("Choose Password", type="password")

        if st.button("Register"):
            if create_user(new_username, new_password):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists!")

    st.stop()

# ---------------- MAIN DASHBOARD ----------------
st.title("📈 StockAI Professional Dashboard")
st.markdown("AI-powered portfolio management and stock analysis platform")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# Sidebar menu
menu = st.sidebar.selectbox(
    "Choose Module",
    [
        "Dashboard",
        "Portfolio Management",
        "Watchlist Management",
        "Excel Portfolio Import",
        "Intrinsic Value Calculator",
        "DCF Valuation Engine",
        "AI BUY/HOLD/SELL Recommendation",
        "Smart Quality & Valuation Engine",
        "Sector-Adjusted Fair Value Engine",
        "Personalized Portfolio Action Plan",
        "Real-Time Stock Screener",
        "Financial Statement Analysis",
        "News & Sentiment Analysis",
        "AI Earnings Forecast"
    ]
)

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":
    st.header("Portfolio Dashboard")

    holdings = get_portfolio()

    if holdings:
        portfolio_data = []
        for h in holdings:
            portfolio_data.append({
                "Symbol": h[1],
                "Quantity": h[2],
                "Buy Price": h[3]
            })

        df = pd.DataFrame(portfolio_data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No portfolio holdings found.")

# ---------------- PORTFOLIO MANAGEMENT ----------------
elif menu == "Portfolio Management":
    st.header("Portfolio Management")

    tab1, tab2, tab3 = st.tabs(["Add Holding", "View Portfolio", "Delete Holding"])

    with tab1:
        symbol = st.text_input("Stock Symbol")
        quantity = st.number_input("Quantity", min_value=1)
        buy_price = st.number_input("Buy Price", min_value=0.0)

        if st.button("Add Holding"):
            add_holding(symbol, quantity, buy_price)
            st.success(f"{symbol} added to portfolio!")

    with tab2:
        holdings = get_portfolio()
        if holdings:
            df = pd.DataFrame(holdings, columns=["ID", "Symbol", "Quantity", "Buy Price", "Buy Date"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Portfolio is empty.")

    with tab3:
        holding_id = st.number_input("Enter Holding ID to Delete", min_value=1)
        if st.button("Delete Holding"):
            delete_holding(holding_id)
            st.success("Holding deleted successfully!")

# ---------------- WATCHLIST MANAGEMENT ----------------
elif menu == "Watchlist Management":
    st.header("Watchlist Management")

    tab1, tab2 = st.tabs(["Add to Watchlist", "View Watchlist"])

    with tab1:
        symbol = st.text_input("Stock Symbol")
        target_price = st.number_input("Target Price", min_value=0.0)

        if st.button("Add to Watchlist"):
            add_to_watchlist(symbol, target_price)
            st.success(f"{symbol} added to watchlist!")

    with tab2:
        watchlist = get_watchlist()
        if watchlist:
            df = pd.DataFrame(watchlist, columns=["ID", "Symbol", "Target Price", "Alert Enabled"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Watchlist is empty.")

# ---------------- EXCEL IMPORT ----------------
elif menu == "Excel Portfolio Import":
    st.header("Import Portfolio from Excel")

    uploaded_file = st.file_uploader("Choose Excel file", type=["xlsx"])

    if uploaded_file is not None:
        with open("temp_portfolio.xlsx", "wb") as f:
            f.write(uploaded_file.getbuffer())

        import_portfolio_from_excel("temp_portfolio.xlsx")
        st.success("Portfolio imported successfully!")

# ---------------- VALUATION ENGINES ----------------
elif menu == "Intrinsic Value Calculator":
    st.header("Intrinsic Value Calculator")
    calculate_intrinsic_value()

elif menu == "DCF Valuation Engine":
    st.header("DCF Valuation Engine")
    calculate_dcf()

# ---------------- AI ENGINES ----------------
elif menu == "AI BUY/HOLD/SELL Recommendation":
    st.header("AI BUY/HOLD/SELL Recommendation")
    calculate_recommendation()

elif menu == "Smart Quality & Valuation Engine":
    st.header("Smart Quality & Valuation Engine")
    smart_quality_valuation_engine()

elif menu == "Sector-Adjusted Fair Value Engine":
    st.header("Sector-Adjusted Fair Value Engine")
    sector_adjusted_fair_value()

elif menu == "Personalized Portfolio Action Plan":
    st.header("Personalized Portfolio Action Plan")
    personalized_action_plan()

# ---------------- SCREENER ----------------
elif menu == "Real-Time Stock Screener":
    st.header("Real-Time Stock Screener")
    run_realtime_screener()

# ---------------- FINANCIAL ANALYSIS ----------------
elif menu == "Financial Statement Analysis":
    st.header("Financial Statement Analysis")
    financial_statement_analysis()

elif menu == "News & Sentiment Analysis":
    st.header("News & Sentiment Analysis")
    analyze_news_sentiment()

elif menu == "AI Earnings Forecast":
    st.header("AI Earnings Forecast & Multibagger Prediction")
    ai_earnings_forecast()