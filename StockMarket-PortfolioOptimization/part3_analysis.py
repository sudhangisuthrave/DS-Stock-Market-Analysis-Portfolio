import numpy as np
import pandas as pd

# Part 3: Statistical Analysis (Expected Returns & Volatility)
def calculate_stats(daily_returns):
    # calculate expected returns and volatility
    expected_returns = daily_returns.mean() * 252
    volatility = daily_returns.std() * np.sqrt(252)

    # combine stats into DataFrame
    stats = pd.DataFrame({
        "Expected Return": expected_returns,
        "Volatility": volatility
    })
    print(stats)
    return expected_returns, volatility, stats
