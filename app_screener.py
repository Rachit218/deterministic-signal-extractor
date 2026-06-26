import streamlit as st
from math_config import load_local_matrix, calculate_beta, construct_spread, check_stationarity
from data_downloader import download_historical_data

st.set_page_config(page_title="Quant Screener", layout="wide")
st.title("Project 1: Cointegration Screener")

st.sidebar.header("Asset Selection")

asset_1 = st.sidebar.text_input("Asset 1", "KO").upper()
asset_2 = st.sidebar.text_input("Asset 2", "PEP").upper()

if st.sidebar.button("Fetch Fresh Data"):
    with st.spinner(f"Downloading data for {asset_1} and {asset_2}..."):
        download_historical_data(asset_1, asset_2)
    st.cache_data.clear()

df = load_local_matrix()
if df is None or df.empty:
    st.error("Data missing. Please fetch fresh data.")
    st.stop()

if asset_1 not in df.columns or asset_2 not in df.columns:
    st.warning(f"The current data file does not contain both {asset_1} and {asset_2}. Please click 'Fetch Fresh Data' to download them.")
    st.stop()


price_A = df[asset_1]
price_B = df[asset_2]

# Math Execution
beta = calculate_beta(price_A, price_B)
raw_spread = construct_spread(price_A, price_B, beta)
p_value = check_stationarity(raw_spread)

# UI Display
st.subheader("Statistical Gatekeeper")
col1, col2 = st.columns(2)
col1.metric("Calculated Beta", f"{beta:.4f}")
col2.metric("ADF P-Value", f"{p_value:.4f}")

if p_value < 0.05:
    st.success("✅ PASS: The spread is stationary. You may proceed to Project 2 (Extraction).")
else:
    st.error("🚨 FAIL: The spread is a random walk. Do not trade.")

st.line_chart(raw_spread)