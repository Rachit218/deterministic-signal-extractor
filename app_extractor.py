import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math_config import load_local_matrix, calculate_beta, construct_spread
from math_filtering import apply_lowpass_filter, isolate_noise, detect_extrema

st.set_page_config(page_title="Signal Extractor", layout="wide")
st.title("Deterministic Signal Extraction")
st.markdown("Works only on pairs that are Cointegrated")

st.sidebar.header("Filter Engineering")
cutoff_freq = st.sidebar.slider("Low-Pass Cutoff Frequency", 0.01, 0.20, 0.05, 0.01)

# Load existing data
df = load_local_matrix()
if df is None:
    st.error("No data found.")
    st.stop()

asset_1, asset_2 = df.columns[0], df.columns[1]
price_A, price_B = df[asset_1], df[asset_2]

beta = calculate_beta(price_A, price_B)
raw_spread = construct_spread(price_A, price_B, beta)

filtered_wave = apply_lowpass_filter(raw_spread.values, cutoff=cutoff_freq)
isolated_noise = isolate_noise(raw_spread.values, filtered_wave)

peaks, troughs = detect_extrema(filtered_wave, min_distance=15)

# --- UI Display ---
st.subheader(f"Decomposing the {asset_1} / {asset_2} Spread")

col_metric1, col_metric2 = st.columns(2)
col_metric1.metric("Identified Maximas (Short Signals)", len(peaks))
col_metric2.metric("Identified Minimas (Buy Signals)", len(troughs))

st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("**1. The Deterministic Wave & Execution Triggers**")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(raw_spread.index, raw_spread.values, color='lightgray', alpha=0.8, label="Raw Spread")
    ax.plot(raw_spread.index, filtered_wave, color='blue', linewidth=2, label="Filtered Wave")
    
    ax.scatter(raw_spread.index[peaks], filtered_wave[peaks], color='red', s=100, zorder=5, label="Maxima (Short)")
    ax.scatter(raw_spread.index[troughs], filtered_wave[troughs], color='green', s=100, zorder=5, label="Minima (Buy)")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with col2:
    st.markdown("**2. Isolated High-Frequency Noise**")
    noise_df = pd.DataFrame({'Stochastic Noise': isolated_noise}, index=raw_spread.index)
    st.line_chart(noise_df, color=["#800080"])