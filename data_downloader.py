import yfinance as yf
import pandas as pd
import os

def download_historical_data(asset_a = 'KO',asset_b = 'PEP'):
    print("Downloading historical data from Yahoo Finance...")
    
    data = yf.download([asset_a, asset_b], period="2y", interval="1d")['Close']
    data = data.dropna()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'historical_prices.csv')
    data.to_csv(file_path)
    
    print(f"Success! Data perfectly downloaded and saved")

if __name__ == "__main__":
    download_historical_data()