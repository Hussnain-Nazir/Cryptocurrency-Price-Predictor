"""
CryptoVision — pages/PREDICTOR.py
Streamlit page: LSTM price forecasting dashboard.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import streamlit as st
from config.theme import inject_theme
from core.market_data import load_coin_registry
from ui.components.sidebar import render_sidebar
from ui.views.predictor import render_predictor

st.set_page_config(
    page_title="CryptoVision – PREDICTOR",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()

# Load coin registry
registry = load_coin_registry()
if not registry:
    st.error(
        "Coin registry not found. "
        "Please ensure `data/raw/coin_registry.csv` exists. "
        "Run `data/scripts/build_coin_registry.py` to regenerate it."
    )
    st.stop()

# Sidebar
controls = render_sidebar(registry)

# Main area
if controls["run"]:
    render_predictor(controls)
else:
    # Idle state — shown before the user clicks Run
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
            text-align: center;
            gap: 14px;
        ">
          <div style="
            width: 56px; height: 56px;
            background: #1E2026;
            border: 1px solid #2B2F36;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
          ">◈</div>
          <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: #EAECEF;
            letter-spacing: 0.02em;
          ">CryptoVision</div>
          <div style="
            font-family: 'Barlow', sans-serif;
            font-size: 0.82rem;
            color: #848E9C;
            max-width: 340px;
            line-height: 1.55;
          ">
            Select an asset and configure the model parameters in the sidebar,
            then click <strong style="color:#F0B90B;">Predict</strong> to generate your forecast.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
