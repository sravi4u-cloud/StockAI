from database.db_manager import (
    add_to_watchlist,
    get_watchlist,
    delete_from_watchlist
)
import streamlit as st
import pandas as pd
import plotly.express as px
import yfinance as yf

from screener.realtime_screener import run_realtime_screener
# Sidebar Watchlist
st.sidebar.title("⭐ My Watchlist")

watchlist = get_watchlist()

if watchlist:
    for item in watchlist:
        st.sidebar.write(f"• {item[1]} — Target: ₹{item[2]}")
else:
    st.sidebar.info("No stocks in watchlist")

st.sidebar.divider()

# Add to Watchlist
st.sidebar.subheader("Add Stock")

watch_symbol = st.sidebar.text_input("Stock Symbol (e.g. INFY.NS)")
watch_target = st.sidebar.number_input("Target Price", min_value=0.0)

if st.sidebar.button("Add to Watchlist"):
    if watch_symbol and watch_target > 0:
        add_to_watchlist(watch_symbol.upper(), watch_target)
        st.sidebar.success(f"Added {watch_symbol} to watchlist!")
        st.rerun()
st.set_page_config(
    page_title="StockAI Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 StockAI Professional Dashboard")
st.markdown("AI-powered stock research, fair value analysis, and portfolio analytics")

# Run screener
if st.button("🚀 Run AI Screener"):
    with st.spinner("Scanning NSE stocks..."):
        results = run_realtime_screener()

    if results:
        df = pd.DataFrame(results)

        # Filter BUY opportunities
        buy_df = df[df["action"] == "BUY"]

        # Top metrics
        st.subheader("📊 Market Summary")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Stocks Scanned", len(df))
        col2.metric("BUY Signals", len(buy_df))
        col3.metric("Best Score", int(df["score"].max()))
        col4.metric("Avg Upside", f"{buy_df['upside'].mean():.1f}%")

        st.divider()

        # Top BUY Opportunities
        st.subheader("🏆 Top AI BUY Opportunities")

        st.dataframe(
            buy_df[[
                "symbol", "price", "fair_value",
                "upside", "score", "action"
            ]],
            width="stretch"
        )

        st.divider()

        # AI Score Distribution Chart
        st.subheader("📈 AI Score Distribution")

        score_chart = px.bar(
            buy_df.sort_values("score", ascending=False),
            x="symbol",
            y="score",
            title="Top BUY Stocks by AI Score",
            text="score"
        )

        score_chart.update_layout(
            xaxis_title="Stock",
            yaxis_title="AI Score",
            height=400
        )

        st.plotly_chart(score_chart, width="stretch")

        st.divider()

        # Portfolio Allocation Pie Chart
        st.subheader("🥧 Portfolio Allocation (Top BUY Opportunities)")

        buy_df["allocation"] = buy_df["score"] / buy_df["score"].sum() * 100

        pie_chart = px.pie(
            buy_df,
            names="symbol",
            values="allocation",
            title="Suggested Allocation Based on AI Score"
        )

        pie_chart.update_layout(height=500)

        st.plotly_chart(pie_chart, width="stretch")

        st.divider()

        # Interactive Stock Price Chart
        st.subheader("📉 Interactive Stock Price Chart")

        selected_stock = st.selectbox(
            "Select a stock to view historical price chart:",
            buy_df["symbol"].tolist()
        )

        if selected_stock:
            stock_data = yf.download(selected_stock, period="6mo")

            if not stock_data.empty:

                # Flatten MultiIndex columns if present
                if isinstance(stock_data.columns, pd.MultiIndex):
                    stock_data.columns = stock_data.columns.get_level_values(0)

                price_chart = px.line(
                    stock_data.reset_index(),
                    x="Date",
                    y="Close",
                    title=f"{selected_stock} - 6 Month Price Chart"
                )

                price_chart.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Price (₹)",
                    height=500
                )

                st.plotly_chart(price_chart, width="stretch")

        st.success(f"Found {len(buy_df)} BUY opportunities!")

else:
    st.info("Click 'Run AI Screener' to start scanning NSE stocks and view the professional dashboard.")
