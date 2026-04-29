"""
MVP Scope — Portfolio Tracker Dashboard

This app will allow users to:
1. Enter asset ticker/name and quantity.
2. Fetch current stock prices using yfinance.
3. Fetch current crypto prices using CoinGecko.
4. Calculate current value per holding.
5. Calculate total portfolio value.
6. Show percentage allocation per asset.
7. Display a simple portfolio allocation chart.
8. Display a simple historical performance chart.

Out of scope for MVP:
- Login system
- Database
- Buying/selling transactions
- Tax calculations
- Advanced risk analytics
- Real-time auto-refresh
"""
import streamlit as st
import pandas as pd

from data import get_stock_data


st.set_page_config(
    page_title="Portfolio Tracker Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Portfolio Tracker Dashboard")

st.write(
    "Enter your stock or crypto holdings in the sidebar to calculate your current portfolio value."
)

st.sidebar.header("Your Holdings")

tickers = []
quantities = []

for i in range(5):
    st.sidebar.subheader(f"Asset {i + 1}")

    ticker = st.sidebar.text_input(
        label=f"Ticker {i + 1}",
        placeholder="Example: AAPL or BTC-USD",
        key=f"ticker_{i}"
    )

    quantity = st.sidebar.number_input(
        label=f"Quantity {i + 1}",
        min_value=0.0,
        value=0.0,
        step=0.1,
        key=f"quantity_{i}"
    )

    if ticker and quantity > 0:
        tickers.append(ticker.upper())
        quantities.append(quantity)


if tickers:
    portfolio_df = get_stock_data(tickers, quantities)

    st.subheader("Portfolio Summary")

    total_portfolio_value = portfolio_df["total_value"].sum()

    st.metric(
        label="Total Portfolio Value",
        value=f"${total_portfolio_value:,.2f}"
    )

    st.dataframe(portfolio_df, use_container_width=True)

else:
    st.info("Enter at least one asset in the sidebar to get started.")