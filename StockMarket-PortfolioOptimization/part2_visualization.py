import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Stock Close Price Over Time
def plot_close_prices(stock_data):
    fig = px.line(stock_data, x="Date", y="Adj Close", color="Ticker",
                  title="Adjusted Close Price Over Time")
    return fig

# Moving Averages and Volume
def plot_moving_averages(stock_data, short_window=50, long_window=200):
    stock_data = stock_data.copy()
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    figs = {}
    for ticker in stock_data['Ticker'].unique():
        ticker_data = stock_data[stock_data['Ticker'] == ticker].copy()
        ticker_data['50_MA'] = ticker_data['Adj Close'].rolling(short_window).mean()
        ticker_data['200_MA'] = ticker_data['Adj Close'].rolling(long_window).mean()

        # Price + MA
        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['Adj Close'],
                                       mode="lines", name="Adj Close"))
        fig_price.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['50_MA'],
                                       mode="lines", name="50-Day MA"))
        fig_price.add_trace(go.Scatter(x=ticker_data['Date'], y=ticker_data['200_MA'],
                                       mode="lines", name="200-Day MA"))
        fig_price.update_layout(title=f"{ticker} - Adj Close & Moving Averages")

        # Volume
        fig_vol = px.bar(ticker_data, x="Date", y="Volume",
                         title=f"{ticker} - Volume Traded")

        figs[ticker] = (fig_price, fig_vol)

    return figs

# Daily Returns Distribution
def plot_returns_distribution(stock_data):
    stock_data['Daily Return'] = stock_data.groupby('Ticker')['Adj Close'].pct_change()
    fig = px.histogram(stock_data, x="Daily Return", color="Ticker", nbins=50, marginal="box",
                       opacity=0.6, title="Distribution of Daily Returns")
    return fig, stock_data

# Correlation Heatmap
def plot_correlation(stock_data):
    daily_returns = stock_data.pivot_table(index="Date", columns="Ticker", values="Daily Return")
    corr = daily_returns.corr()
    fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                    title="Correlation Matrix of Daily Returns")
    return fig, daily_returns
