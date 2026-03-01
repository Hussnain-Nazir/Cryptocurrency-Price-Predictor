"""
ChainVision — core/market_data.py
Handles loading coin registry and fetching OHLCV history from Yahoo Finance.
"""

import os
import pandas as pd
import yfinance as yf
import streamlit as st


# Constants
_REGISTRY_PATH = os.path.join(
    os.path.dirname(__file__), "..", "data", "raw", "coin_registry.csv"
)


# Coin registry
@st.cache_data(show_spinner=False)
def load_coin_registry() -> list[dict]:
    """
    Read the local CSV of coin tickers and names, returning a list of dicts.
    Each dict has keys 'ticker' and 'name'.
    """
    registry_file = os.path.abspath(_REGISTRY_PATH)
    try:
        frame = pd.read_csv(registry_file)
        needed = {"ticker", "name"}
        missing = needed - set(frame.columns)
        if missing:
            raise ValueError(f"Registry CSV is missing columns: {missing}")
        return frame[["ticker", "name"]].dropna().to_dict(orient="records")

    except FileNotFoundError:
        st.error(
            f"Coin registry not found at `{registry_file}`. "
            "Run `data/scripts/fetch_coin_registry.py` to regenerate it."
        )
        return []
    except Exception as exc:
        st.error(f"Failed to load coin registry: {exc}")
        return []


# Price history
def fetch_price_history(ticker: str) -> tuple[pd.DataFrame, str]:
    """
    Download full daily OHLCV history for *ticker* via yfinance.
    Returns (dataframe, close_column_name).
    Raises ValueError when no usable data is available.
    """
    raw = yf.download(ticker, period="max", interval="1d", progress=False)

    if raw.empty:
        raise ValueError(f"Yahoo Finance returned no data for '{ticker}'.")

    # Flatten MultiIndex columns that yfinance sometimes produces
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = ["_".join(col).strip() for col in raw.columns]

    # Resolve close column name
    if "Close" in raw.columns:
        close_col = "Close"
    elif f"Close_{ticker}" in raw.columns:
        close_col = f"Close_{ticker}"
    else:
        raise ValueError(
            f"Cannot locate a 'Close' price column for '{ticker}'. "
            f"Available columns: {list(raw.columns)}"
        )

    cleaned = raw.dropna(subset=[close_col])
    if cleaned.empty:
        raise ValueError(f"All rows have NaN closing prices for '{ticker}'.")

    return cleaned, close_col


# Small helpers
def format_prediction_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tidy a future-predictions DataFrame for display:
    • Remove duplicate columns
    • Format dates as YYYY-MM-DD strings
    • Rename the price column to something human-readable
    """
    df = df.loc[:, ~df.columns.duplicated()].copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df = df.rename(columns={"Predicted Price": "Forecast (USD)"})
    return df.reset_index(drop=True)
