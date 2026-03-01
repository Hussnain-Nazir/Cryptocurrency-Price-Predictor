"""
CryptoVision — ui/views/home.py
Home page: introduction, feature overview, usage guide.
"""

import streamlit as st
from config.theme import PALETTE


# Private helpers
def _section_title(text: str) -> None:
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 32px 0 16px 0;
        ">
          <div style="
            width: 3px;
            height: 18px;
            background: {PALETTE['accent']};
            border-radius: 2px;
            flex-shrink: 0;
          "></div>
          <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 1.0rem;
            font-weight: 700;
            color: {PALETTE['text_primary']};
            letter-spacing: 0.04em;
            text-transform: uppercase;
          ">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _feature_card(icon: str, title: str, description: str) -> str:
    return f"""
    <div style="
        background: {PALETTE['bg_surface']};
        border: 1px solid {PALETTE['border_light']};
        border-top: 2px solid {PALETTE['accent']};
        border-radius: 4px;
        padding: 18px 16px;
        height: 100%;
    ">
      <div style="font-size: 1.3rem; margin-bottom: 10px; line-height: 1;">{icon}</div>
      <div style="
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: {PALETTE['text_primary']};
        letter-spacing: 0.02em;
        margin-bottom: 6px;
        text-transform: uppercase;
      ">{title}</div>
      <div style="
        font-family: 'Barlow', sans-serif;
        font-size: 0.8rem;
        color: {PALETTE['text_secondary']};
        line-height: 1.55;
      ">{description}</div>
    </div>
    """


def _step_row(number: str, title: str, detail: str) -> str:
    return f"""
    <div style="
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 13px 16px;
        background: {PALETTE['bg_surface']};
        border: 1px solid {PALETTE['border_light']};
        border-radius: 4px;
        margin-bottom: 8px;
    ">
      <div style="
        min-width: 26px;
        height: 26px;
        background: {PALETTE['accent']};
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.78rem;
        font-weight: 700;
        color: {PALETTE['text_inverse']};
        flex-shrink: 0;
        margin-top: 1px;
      ">{number}</div>
      <div>
        <div style="
          font-family: 'Barlow', sans-serif;
          font-size: 0.88rem;
          font-weight: 600;
          color: {PALETTE['text_primary']};
          margin-bottom: 2px;
        ">{title}</div>
        <div style="
          font-family: 'Barlow', sans-serif;
          font-size: 0.78rem;
          color: {PALETTE['text_secondary']};
          line-height: 1.45;
        ">{detail}</div>
      </div>
    </div>
    """


# Main renderer
def render_home() -> None:

    # Hero banner
    st.markdown(
        f"""
        <div style="
            background: {PALETTE['bg_surface']};
            border: 1px solid {PALETTE['border_light']};
            border-left: 4px solid {PALETTE['accent']};
            border-radius: 4px;
            padding: 28px 28px 24px 28px;
            margin-bottom: 8px;
        ">
          <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
          ">
            <div style="
              width: 32px; height: 32px;
              background: {PALETTE['accent']};
              border-radius: 6px;
              display: flex; align-items: center;
              justify-content: center;
              font-size: 16px;
              flex-shrink: 0;
            ">◈</div>
            <h1 style="
              font-family: 'Barlow Condensed', sans-serif !important;
              font-size: 1.85rem !important;
              font-weight: 700 !important;
              color: {PALETTE['text_primary']} !important;
              letter-spacing: 0.02em;
              margin: 0 !important;
            ">CryptoVision</h1>
          </div>
          <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: {PALETTE['accent']};
            margin-bottom: 14px;
          ">Cryptocurrency Price Predictor</div>
          <p style="
            font-family: 'Barlow', sans-serif;
            font-size: 0.95rem;
            color: {PALETTE['text_secondary']};
            line-height: 1.65;
            max-width: 700px;
            margin: 0;
          ">
            CryptoVision uses a stacked LSTM (Long Short-Term Memory) neural network
            trained on full historical daily price data to forecast cryptocurrency prices
            up to 90 days ahead. Select any of the 1,000 supported coins, configure the
            model, and get an interactive price forecast in minutes.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Market disclaimer ribbon
    st.markdown(
        f"""
        <div style="
            background: {PALETTE['bear_bg']};
            border: 1px solid {PALETTE['bear']};
            border-radius: 4px;
            padding: 8px 14px;
            margin-bottom: 4px;
            font-family: 'Barlow', sans-serif;
            font-size: 0.75rem;
            color: {PALETTE['bear']};
            display: flex;
            align-items: center;
            gap: 8px;
        ">
          <span>⚠</span>
          <span>Forecasts are for educational purposes only.
          This tool does not provide financial advice.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Features
    _section_title("What CryptoVision Does")

    feature_cols = st.columns(3)
    features = [
        ("📡", "Live Price Data",
         "Pulls the complete OHLCV history directly from Yahoo Finance for accurate, up-to-date training data."),
        ("🧠", "LSTM Neural Network",
         "Two stacked LSTM layers with a 60-day lookback window learn temporal price patterns from historical data."),
        ("📈", "Interactive Forecast",
         "Results visualised as a Plotly overlay chart showing historical prices, model fit, and future prediction."),
        ("🎯", "Adjustable Horizon",
         "Predict 1 to 90 days into the future using the sidebar slider — short-term or medium-term views."),
        ("⚙️", "Tunable Training",
         "Control training depth from 1 to 50 epochs. More epochs improve fit at the cost of longer runtime."),
        ("💾", "CSV Export",
         "Download the day-by-day forecast table as a CSV file for offline analysis or record keeping."),
    ]
    for idx, (icon, title, desc) in enumerate(features):
        with feature_cols[idx % 3]:
            st.markdown(_feature_card(icon, title, desc), unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # How to use
    _section_title("How to Use the Predictor")

    steps = [
        ("1", "Open the Predictor page", "Navigate to the Predictor page using the sidebar navigation on the left."),
        ("2", "Select a cryptocurrency", "Use the Asset dropdown in the sidebar to choose from 1,000 coins sorted by market cap."),
        ("3", "Set training epochs", "Adjust the Epochs slider — 10 is a good default; increase for potentially better accuracy."),
        ("4", "Set forecast horizon", "Choose how many days ahead you want to predict (1–90 days)."),
        ("5", "Run the prediction", "Click Run Prediction. The model will fetch data, train, and generate results."),
        ("6", "Analyse the results", "Review the forecast chart, summary stats, and the day-by-day price table. Download the CSV if needed."),
    ]

    for num, title, detail in steps:
        st.markdown(_step_row(num, title, detail), unsafe_allow_html=True)

    # About the model
    _section_title("About the Model")

    st.markdown(
        f"""
        <div style="
            background: {PALETTE['bg_surface']};
            border: 1px solid {PALETTE['border_light']};
            border-radius: 4px;
            padding: 20px 22px;
        ">
          <div style="
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px 32px;
          ">
            {''.join([
                f'<div><div style="font-family:DM Mono,monospace;font-size:0.68rem;'
                f'color:{PALETTE["text_muted"]};letter-spacing:0.1em;'
                f'text-transform:uppercase;margin-bottom:3px;">{k}</div>'
                f'<div style="font-family:Barlow,sans-serif;font-size:0.875rem;'
                f'color:{PALETTE["text_primary"]};font-weight:500;">{v}</div></div>'
                for k, v in [
                    ("Architecture", "2-layer Stacked LSTM"),
                    ("Units per Layer", "50 neurons"),
                    ("Lookback Window", "60 trading days"),
                    ("Train / Test Split", "80% / 20%"),
                    ("Sequence Length", "60 timesteps → 1 output"),
                    ("Loss Function", "Mean Squared Error"),
                    ("Optimiser", "Adam"),
                    ("Scaler", "MinMax (0 → 1)"),
                ]
            ])}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
