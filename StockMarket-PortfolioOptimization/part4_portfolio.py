import numpy as np
import pandas as pd
import plotly.express as px

def portfolio_performance(weights, returns, cov_matrix):
    p_return = np.dot(weights, returns)
    p_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return p_return, p_volatility

def simulate_portfolios(expected_returns, daily_returns, num_portfolios=5000):
    results = np.zeros((3, num_portfolios))
    cov_matrix = daily_returns.cov() * 252
    tickers = expected_returns.index

    np.random.seed(42)
    weights_list = []
    for i in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        ret, vol = portfolio_performance(weights, expected_returns, cov_matrix)
        results[0, i] = ret
        results[1, i] = vol
        results[2, i] = ret / vol
        weights_list.append(weights)

    df = pd.DataFrame(weights_list, columns=tickers)
    df["Return"], df["Volatility"], df["Sharpe"] = results[0], results[1], results[2]

    fig = px.scatter(df, x="Volatility", y="Return", color="Sharpe",
                     title="Efficient Frontier", color_continuous_scale="Viridis")
    return results, cov_matrix, fig

def find_max_sharpe(results):
    idx = np.argmax(results[2])
    return results[0, idx], results[1, idx], results[2, idx]

def get_optimal_weights(results, max_sharpe_ratio, expected_returns, cov_matrix, num_portfolios=5000):
    tickers = expected_returns.index
    np.random.seed(42)

    for i in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        ret, vol = portfolio_performance(weights, expected_returns, cov_matrix)
        if results[2, i] == max_sharpe_ratio:
            return pd.DataFrame({"Ticker": tickers, "Weight": weights})
    return None
