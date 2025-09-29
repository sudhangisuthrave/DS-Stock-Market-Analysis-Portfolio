import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np

# -------------------------------
# Streamlit App Layout
# -------------------------------
st.set_page_config(page_title="Stock Market Analysis", layout="wide")
st.title("📈 Stock Market Interactive Dashboard")

# -------------------------------
# User Inputs
# -------------------------------
tickers_input = st.text_input(
    "Enter stock tickers (comma-separated, e.g., AAPL, MSFT, TSLA, INFY.NS):",
    value="AAPL, MSFT, TSLA"
)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

date_range = st.date_input(
    "Select Date Range:",
    value=[pd.to_datetime("2024-01-01"), pd.to_datetime("today")]
)
start_date, end_date = date_range

# -------------------------------
# Download Data
# -------------------------------
if tickers:
    data = yf.download(tickers, start=start_date, end=end_date, group_by="ticker", auto_adjust=True)

    # Convert to long format for easier handling
    if len(tickers) == 1:
        df = data.copy()
        df["Ticker"] = tickers[0]
    else:
        df = pd.concat([data[t].assign(Ticker=t) for t in tickers], axis=0)

    df.reset_index(inplace=True)

    # Daily Return
    df["Daily Return"] = df.groupby("Ticker")["Close"].pct_change()

    # -------------------------------
    # Download Option
    # -------------------------------
    st.subheader("📥 Download Data")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="stock_data.csv",
        mime="text/csv"
    )

    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Stock Data")
    st.download_button(
        label="Download Excel",
        data=excel_buffer,
        file_name="stock_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # -------------------------------
    # Expected Return & Volatility
    # -------------------------------
    st.subheader("📊 Expected Return & Volatility")
    daily_returns = df.pivot_table(index="Date", columns="Ticker", values="Daily Return")
    expected_returns = daily_returns.mean() * 252  # Annualized
    volatility = daily_returns.std() * np.sqrt(252)  # Annualized

    stats_df = pd.DataFrame({
        "Expected Return": expected_returns,
        "Volatility": volatility
    })
    st.dataframe(stats_df.style.format("{:.2%}"))

    # -------------------------------
    # Plot 1: Adjusted Close
    # -------------------------------
    st.subheader("Adjusted Close Prices")
    fig = px.line(df, x="Date", y="Close", color="Ticker", title="Stock Prices Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Plot 2: Volume
    # -------------------------------
    st.subheader("Trading Volume")
    fig = px.bar(df, x="Date", y="Volume", color="Ticker", title="Trading Volume")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Plot 3: Daily Returns Distribution
    # -------------------------------
    st.subheader("Daily Returns Distribution")
    fig = px.histogram(
        df, x="Daily Return", color="Ticker", nbins=50, marginal="box",
        title="Distribution of Daily Returns"
    )
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Plot 4: Moving Averages
    # -------------------------------
    st.subheader("Moving Averages (50 & 200 days)")
    ma_df = df.copy()
    ma_df["50_MA"] = ma_df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(50).mean())
    ma_df["200_MA"] = ma_df.groupby("Ticker")["Close"].transform(lambda x: x.rolling(200).mean())

    fig = px.line(ma_df, x="Date", y=["Close", "50_MA", "200_MA"], color="Ticker",
                  title="Moving Averages")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Plot 5: Correlation Heatmap
    # -------------------------------
    st.subheader("Correlation Heatmap of Daily Returns")
    corr = daily_returns.corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

else:
    st.warning("Please enter at least one stock ticker.")
