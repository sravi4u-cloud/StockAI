import streamlit as st
from auth.auth_manager import create_user, verify_user

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Login/Register page
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
            create_user(new_username, new_password)
            st.success("Account created! Please login.")

    st.stop()
import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_manager import get_portfolio
from data.stock_fetcher import fetch_stock_data

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
st.set_page_config(
    page_title="StockAI Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("📈 StockAI Professional Dashboard")
st.markdown("AI-powered portfolio management and stock analysis platform")

# ---------------- LOAD PORTFOLIO ----------------
holdings = get_portfolio()

if holdings:
    portfolio_data = []
    total_investment = 0
    total_current_value = 0

    for holding in holdings:
        _, symbol, quantity, buy_price, _ = holding

        stock_data = fetch_stock_data(symbol)

        if stock_data:
            current_price = stock_data["current_price"]
            current_value = quantity * current_price
            investment = quantity * buy_price
            pnl = current_value - investment

            total_investment += investment
            total_current_value += current_value

            portfolio_data.append({
                "Symbol": symbol,
                "Quantity": quantity,
                "Buy Price": buy_price,
                "Current Price": round(current_price, 2),
                "Investment": round(investment, 2),
                "Current Value": round(current_value, 2),
                "P&L": round(pnl, 2),
                "Sector": stock_data.get("sector", "Unknown")
            })

    df = pd.DataFrame(portfolio_data)

    # ---------------- METRICS ----------------
    total_pnl = total_current_value - total_investment
    total_return = (total_pnl / total_investment) * 100 if total_investment > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Investment", f"₹{total_investment:,.0f}")
    col2.metric("Current Value", f"₹{total_current_value:,.0f}")
    col3.metric("Total P&L", f"₹{total_pnl:,.0f}", f"{total_return:.2f}%")
    col4.metric("Holdings", len(df))

    # ---------------- PORTFOLIO TABLE ----------------
    st.subheader("Portfolio Holdings")
    st.dataframe(df, use_container_width=True)

    # ---------------- CHARTS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sector Allocation")
        sector_df = df.groupby("Sector")["Current Value"].sum().reset_index()
        fig = px.pie(
            sector_df,
            values="Current Value",
            names="Sector",
            title="Portfolio by Sector"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top Holdings")
        top_df = df.sort_values("Current Value", ascending=False).head(10)
        fig = px.bar(
            top_df,
            x="Symbol",
            y="Current Value",
            title="Top 10 Holdings by Value"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- GAINERS / LOSERS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Gainers")
        gainers = df.sort_values("P&L", ascending=False).head(5)
        st.dataframe(gainers[["Symbol", "P&L"]], use_container_width=True)

    with col2:
        st.subheader("Top Losers")
        losers = df.sort_values("P&L").head(5)
        st.dataframe(losers[["Symbol", "P&L"]], use_container_width=True)

else:
    st.warning("No portfolio holdings found. Please add or import your portfolio first.")

# ---------------- STOCK ANALYSIS ----------------
st.subheader("🔍 Real-Time Stock Analysis")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., HAL, SBIN, INFY)")

if st.button("Analyze Stock") and symbol:
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    stock_data = fetch_stock_data(symbol)

    if stock_data:
        col1, col2, col3 = st.columns(3)

        col1.metric("Current Price", f"₹{stock_data['current_price']:.2f}")
        col2.metric("P/E Ratio", f"{stock_data['pe_ratio']:.2f}")
        col3.metric("ROE", f"{stock_data['roe']*100:.2f}%")

        st.write("### Company Information")
        st.write(f"**Company:** {stock_data.get('company_name', 'N/A')}")
        st.write(f"**Sector:** {stock_data.get('sector', 'N/A')}")
        st.write(f"**Market Cap:** ₹{stock_data.get('market_cap', 0)/1e7:,.0f} Cr")

    else:
        st.error("Could not fetch stock data.")