import pandas as pd
import yfinance as yf
from datetime import date, timedelta

# Part 1: Data Download & Preparation
def load_stock_data(tickers, lookback_days=365):
    # define the time period for the data
    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=lookback_days)).strftime("%Y-%m-%d")

    # download stock data from Yahoo Finance
    data = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=False
    ).reset_index()

    # flatten MultiIndex columns
    data.columns = ['Date'] + [f"{attr}_{ticker}" for attr, ticker in data.columns[1:]]

    # melt the DataFrame to make it long format where each row is a unique combination of Date, Ticker, and attributes
    melted = data.melt(id_vars=['Date'], var_name='Attribute_Ticker', value_name='Value')
    melted[['Attribute', 'Ticker']] = melted['Attribute_Ticker'].str.split('_', expand=True)
    melted = melted.drop(columns=['Attribute_Ticker'])

    # pivot the melted DataFrame to have the attributes (Open, High, Low, etc.) as columns
    pivoted = melted.pivot_table(
        index=['Date', 'Ticker'],
        columns='Attribute',
        values='Value',
        aggfunc='first'
    )

    # reset index to turn multi-index into columns
    stock_data = pivoted.reset_index()
    return stock_data
