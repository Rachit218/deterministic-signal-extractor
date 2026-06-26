import statsmodels.api as sm
import os
import pandas as pd
from statsmodels.tsa.stattools import adfuller

def load_local_matrix():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'historical_prices.csv')
    if not os.path.exists(file_path):
        return None
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data

def calculate_beta(price_a, price_b):
    B_with_const = sm.add_constant(price_b)
    model = sm.OLS(price_a, B_with_const).fit()
    beta = model.params.iloc[1]
    return beta

def construct_spread(price_a, price_b, beta):
    return price_a - (beta * price_b)

def check_stationarity(spread):
    adf_result = adfuller(spread)
    p_value = adf_result[1]
    return p_value