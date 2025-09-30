# DS-Stock-Market-Analysis-Portfolio
DS-Interactive Stock Market Analysis &amp; Portfolio Dashboard

# 📈 Interactive Stock Market Analysis & Portfolio Dashboard

An interactive Streamlit web application for stock market analysis and portfolio optimization. This dashboard allows users to explore stock prices, moving averages, daily returns, correlations, and download historical stock data.

Built with Python, Streamlit, Plotly, Seaborn, and yFinance.

# 🚀 Features

Custom Tickers – Users can type in any ticker(s) supported by Yahoo Finance.
Custom Date Ranges – Select start and end dates for analysis.
Interactive Charts –
  Adjusted Close Prices (line chart)
  Trading Volume (bar chart)
  Moving Averages (50-day & 200-day)
  Daily Returns Distribution (histogram with box plot)
  Correlation Heatmap of daily returns
Expected Return & Volatility – Calculates annualized return and volatility for selected tickers.
Download Options – Export stock data to CSV or Excel.


# 📦 Installation

Clone the repository:

git clone https://github.com/sudhangisuthrave/stock-analysis-dashboard.git

cd stock-analysis-dashboard


# Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


# Install required packages:

pip install streamlit yfinance plotly seaborn matplotlib pandas

# ⚡ Usage

Run the Streamlit app:

streamlit run app.py


The app will open in your default browser.
Enter tickers (comma-separated), pick a date range, and explore the interactive charts.
Download data using the CSV or Excel buttons.


# 🔧 Dependencies

Python 3.9+

streamlit

yfinance

pandas

plotly

seaborn

matplotlib

xlsxwriter (for Excel export)
