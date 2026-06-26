# Quantitative Statistical Arbitrage: Signal Extractor

This repository contains the second phase of a two-part statistical arbitrage pipeline. Assuming a pair has already passed a strict Augmented Dickey-Fuller (ADF) cointegration test, this tool applies advanced digital signal processing (DSP) to isolate the deterministic structural wave from stochastic market noise, identifying mathematically precise execution triggers.

---

## The Mathematics of Signal Extraction

Financial market prices are heavily polluted by high-frequency microstructure noise (e.g., bid-ask bounces, HFT latency arbitrage). To build a systematic trading strategy, we must isolate the true underlying economic tether.

### 1. Wold's Representation Theorem
By mathematically proving the spread is stationary (via Project 1's Gatekeeper), we satisfy the prerequisite for Wold's Theorem, allowing us to decompose the time series ($y_t$) into a deterministic component and a stochastic component:
$$y_t = x_{\text{deterministic}} + v_{\text{stochastic}}$$

### 2. Zero-Phase Low-Pass Filtering
To extract $x_{\text{deterministic}}$, the algorithm applies a **Butterworth Low-Pass Filter**. 
* We utilize `scipy.signal.filtfilt` to apply the filter in both the forward and reverse directions. 
* This zero-phase filtering ensures there is **no phase shift** (time lag), aligning the extracted wave perfectly with the historical price data for accurate backtesting.

### 3. Calculus-Based Execution Triggers
Arbitrary visual thresholds (e.g., trading when the spread crosses 2 standard deviations) are sub-optimal. This engine mathematically pinpoints maximum stretch conditions by finding the local extrema of the filtered wave where the first derivative is zero:
$$f'(x_{\text{filtered}}) = 0$$
* **Local Maxima (Red Triggers):** The positive anomaly has peaked; trigger a **Short Spread** execution.
* **Local Minima (Green Triggers):** The negative anomaly has bottomed; trigger a **Buy Spread** execution.

---

## Technical Architecture
* **Signal Processing Backend:** `scipy.signal` handles the digital filter.
* **Calculus Engine:** Extrema detection.
* **Interactive Frontend:** Built with `streamlit` and `matplotlib`.

---

## Quick Start & Usage

**1. Clone the repository and navigate to the directory:**
`git clone https://github.com/Rachit218/deterministic-signal-extractor.git`
`cd deterministic-signal-extractor`

**2. Install the required quantitative libraries:**
`pip install pandas yfinance statsmodels scipy matplotlib streamlit`

**3. Populate the data:**
`python data_downloader.py`

**4. Launch the Dashboard:**
`streamlit run app_extractor.py`

*(Note: In the UI, use the sidebar to fetch 1-year historical data for known cointegrated pairs like BRK-A and BRK-B before tuning the filter).*

---
