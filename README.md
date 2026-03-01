# ◈ CryptoVision – Cryptocurrency Price Predictor

> A professional LSTM-powered cryptocurrency price forecasting dashboard built with Python and Streamlit.

---

## Overview

CryptoVision is a machine learning web application that forecasts cryptocurrency closing prices using a two-layer stacked LSTM (Long Short-Term Memory) neural network. It pulls full historical OHLCV data from Yahoo Finance, trains a model on the fly, and presents an interactive price forecast through a Binance-inspired dark trading dashboard.

The project is designed as a portfolio demonstration of end-to-end ML pipeline development: data ingestion, sequence modelling, interactive visualisation, and technical analysis — all within a clean, professional UI.

---

## Key Features

- **1,000 supported coins** — Top assets by market cap, pre-loaded from CoinGecko
- **Live data** — Full OHLCV history pulled in real time via Yahoo Finance
- **LSTM model** — Two stacked LSTM layers (50 units each), 60-day lookback, 80/20 train-test split
- **Configurable training** — Adjust epochs (1–50) and forecast horizon (1–90 days) from the sidebar
- **Three-trace forecast chart** — Historical prices, model back-test fit, and future forecast overlaid in one view
- **Market stat cards** — Last close, 24h change, all-time high/low, and dataset size at a glance
- **Volume chart** — Trading volume bar chart
- **Moving Average chart** — MA20, MA50, and MA200 overlaid on the closing price for trend analysis
- **RSI chart** — 14-day Relative Strength Index with overbought (70) and oversold (30) reference bands
- **Forecast table** — Day-by-day predicted prices displayed in a sortable table
- **CSV export** — Download the full forecast as a CSV file with one click
- **Intuitive dashboard** — Designed to support efficient navigation and clear data interpretation

---

## Interface

### HOME Page
Introduction to the tool, feature overview, step-by-step usage guide, and a model reference table. Navigate here for context before running a prediction.

### PREDICTOR Page
The main forecasting dashboard. Contains:
- **Asset selector** — Choose any of the 1,000 supported coins
- **Model parameters** — Epoch count and forecast horizon sliders
- **Market overview panel** — Key stats for the selected coin
- **Historical price chart** — Full price history area chart
- **Volume chart** — Trading volume bars in the app accent colour
- **Technical Analysis** — Tabbed section with Moving Average and RSI charts
- **Forecast chart** — Overlay of historical, back-test fit, and future predicted prices
- **Forecast summary** — Start price, end price, and expected percentage change
- **Day-by-day table** — Exportable price-per-day forecast

---

## Installation

### Prerequisites
- Python 3.11
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/your-username/CryptoVision.git
cd CryptoVision
```

**2. Create and activate a virtual environment**
```bash
python3.11 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the application**
```bash
streamlit run HOME.py
```

Open your browser at `http://localhost:8501`.

---

## Refreshing the Coin Registry

The coin registry (`data/raw/coin_registry.csv`) is pre-generated and included. To refresh it with the latest market rankings, run:

```bash
python data/scripts/build_coin_registry.py
```

Or open the Jupyter notebook equivalent:
```
data/scripts/CoinRegistryBuilder.ipynb
```

This fetches the top 1,000 coins by market cap from the CoinGecko public API and overwrites the CSV.

---

## Project Structure

```
CryptoVision/
│
├── HOME.py                        # Entry-point — HOME page
│
├── pages/
│   └── PREDICTOR.py               # PREDICTOR dashboard page
│
├── core/                          # ML & data logic
│   ├── forecast_engine.py         # LSTM build / train / predict pipeline
│   └── market_data.py             # Coin registry loader & yfinance downloader
│
├── ui/                            # Presentation layer
│   ├── components/
│   │   ├── charts.py              # Plotly figure builders (price, forecast, volume, MA, RSI)
│   │   └── sidebar.py             # Sidebar control panel
│   └── views/
│       ├── home.py                # HOME page layout & content
│       └── predictor.py           # PREDICTOR dashboard layout
│
├── config/
│   └── theme.py                   # Design tokens, colour palette & CSS injection
│
├── data/
│   ├── raw/
│   │   └── coin_registry.csv      # 1,000 coins: ticker, name
│   └── scripts/
│       ├── build_coin_registry.py # CLI script to regenerate registry
│       └── CoinRegistryBuilder.ipynb
│
├── requirements.txt
└── README.md
```

---

## How Predictions Work

1. **Data ingestion** — `yfinance` downloads the full daily closing price history for the selected coin (all available data, typically 4–7 years for major coins).

2. **Preprocessing** — Prices are normalised to [0, 1] using MinMaxScaler. Sequences of 60 consecutive days are created as input windows.

3. **Training** — An 80% slice of the data trains a two-layer stacked LSTM. Layer 1 returns full sequences; Layer 2 outputs a single value fed through a Dense hidden layer and a final Dense output neuron.

4. **Back-testing** — The trained model runs inference on the held-out 20% test slice, producing a back-test fit line visible on the forecast chart.

5. **Forecasting** — The model predicts autoregressively: each new prediction is appended to the rolling 60-day window, which then feeds the next step. This repeats for the chosen horizon.

6. **Inverse scaling** — All predictions are scaled back to USD before display.

| Parameter | Value |
|---|---|
| Architecture | 2-layer Stacked LSTM |
| Units per layer | 50 |
| Lookback window | 60 days |
| Train / test split | 80% / 20% |
| Loss function | Mean Squared Error |
| Optimiser | Adam |
| Batch size | 1 |

---

## Dependencies

| Package | Version |
|---|---|
| streamlit | 1.40.1 |
| tensorflow-cpu | 2.14.0 |
| keras | 2.14.0 |
| yfinance | latest |
| plotly | 5.17.0 |
| scikit-learn | 1.5.2 |
| pandas | 2.2.3 |
| numpy | 1.26.4 |
| requests | 2.31.0 |

> Python 3.11 is required. TensorFlow 2.14 does not support Python 3.12+.

---

## Environment

Developed and tested on:
- **OS**: Ubuntu 22.04 LTS / macOS 14
- **Python**: 3.11.x
- **CPU inference** — no GPU required

---

## Notes

- **Training time** — With `batch_size=1` and Bitcoin's ~4,000 rows of history, expect roughly 1–3 minutes per epoch on a modern CPU. Start with 5–10 epochs.
- **Yahoo Finance availability** — Data quality and availability vary by coin. Very new or illiquid tokens may return empty results.
- **CoinGecko rate limits** — The free API tier allows ~30 req/min. The registry builder sleeps automatically on HTTP 429 responses.

---

## Disclaimer

**CryptoVision is a portfolio and educational project. All forecasts are generated from historical price data and are for illustrative purposes only. Nothing in this project constitutes financial advice. Past price patterns are not indicative of future results.**
