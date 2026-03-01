"""
CryptoVision — ui/components/sidebar.py
Sidebar control panel
"""

import streamlit as st
from config.theme import PALETTE


# Helpers
def _label(text: str) -> None:
    """Render an uppercase tracking label above a widget."""
    st.markdown(
        f"<span class='cv-sidebar-label'>{text}</span>",
        unsafe_allow_html=True,
    )


def _spacer(px: int = 12) -> None:
    st.markdown(
        f"<div style='height:{px}px'></div>",
        unsafe_allow_html=True,
    )


# Main renderer
def render_sidebar(coin_registry: list[dict]) -> dict:
    """
    Render the sidebar and return user selections as a dict:
        { 'ticker', 'name', 'epochs', 'horizon', 'run' }
    """
    with st.sidebar:

        # Brand header
        st.markdown(
            f"""
            <div style="
                padding: 20px 4px 16px 4px;
                border-bottom: 1px solid {PALETTE['border_light']};
                margin-bottom: 20px;
            ">
              <div style="
                display: flex;
                align-items: center;
                gap: 8px;
                margin-bottom: 4px;
              ">
                <div style="
                  width: 28px; height: 28px;
                  background: {PALETTE['accent']};
                  border-radius: 6px;
                  display: flex; align-items: center; justify-content: center;
                  font-size: 14px; line-height: 1;
                ">◈</div>
                <span style="
                  font-family: 'Barlow Condensed', sans-serif;
                  font-size: 1.25rem;
                  font-weight: 700;
                  color: {PALETTE['text_primary']};
                  letter-spacing: 0.02em;
                ">CryptoVision</span>
              </div>
              <div style="
                font-family: 'Barlow', sans-serif;
                font-size: 0.7rem;
                color: {PALETTE['text_muted']};
                letter-spacing: 0.06em;
                padding-left: 36px;
              ">CRYPTOCURRENCY PRICE PREDICTOR</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Asset selector
        _label("Select Asset")
        options = [f"{d['ticker']}  —  {d['name']}" for d in coin_registry]
        selection = st.selectbox(
            label="asset",
            options=options,
            label_visibility="collapsed",
        )
        selected_ticker = selection.split("—")[0].strip()
        selected_name   = selection.split("—")[1].strip()

        _spacer(16)

        # Divider
        st.markdown(
            f"<hr style='border:none;border-top:1px solid {PALETTE['border_light']};margin:0 0 16px 0;'>",
            unsafe_allow_html=True,
        )

        # Model settings header
        st.markdown(
            f"""
            <div style="
                font-family: 'Barlow Condensed', sans-serif;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: {PALETTE['text_muted']};
                margin-bottom: 14px;
            ">Model Parameters</div>
            """,
            unsafe_allow_html=True,
        )

        # Epochs
        _label("Training Epochs")
        epochs = st.slider(
            label="epochs",
            min_value=1,
            max_value=50,
            value=10,
            label_visibility="collapsed",
        )
        epoch_label = "epochs" if epochs != 1 else "epoch"
        accent = PALETTE["accent"]
        st.markdown(
            f"<div style='font-family:DM Mono,monospace;font-size:0.72rem;"
            f"color:{accent};margin-top:-6px;margin-bottom:14px;'>"
            f"{epochs} {epoch_label}</div>",
            unsafe_allow_html=True,
        )

        # Forecast horizon
        _label("Forecast Horizon")
        horizon = st.slider(
            label="horizon",
            min_value=1,
            max_value=90,
            value=30,
            label_visibility="collapsed",
        )
        day_label = "days" if horizon != 1 else "day"
        st.markdown(
            f"<div style='font-family:DM Mono,monospace;font-size:0.72rem;"
            f"color:{accent};margin-top:-6px;margin-bottom:20px;'>"
            f"{horizon} {day_label} ahead</div>",
            unsafe_allow_html=True,
        )

        # Run button
        run = st.button("Predict")

        # Info note
        _spacer(8)
        st.markdown(
            f"""
            <div style="
                background: {PALETTE['bg_elevated']};
                border: 1px solid {PALETTE['border_light']};
                border-left: 3px solid {PALETTE['accent']};
                border-radius: 4px;
                padding: 10px 12px;
                font-family: 'Barlow', sans-serif;
                font-size: 0.72rem;
                color: {PALETTE['text_muted']};
                line-height: 1.5;
            ">
              Higher epochs improve accuracy<br>but increase training time.
            </div>
            """,
            unsafe_allow_html=True,
        )

        _spacer(16)

        # Disclaimer
        st.markdown(
            f"""
            <hr style='border:none;border-top:1px solid {PALETTE["border_light"]};'>
            <div style="
                font-family: 'Barlow', sans-serif;
                font-size: 0.65rem;
                color: {PALETTE['text_muted']};
                line-height: 1.5;
                padding: 4px 0;
            ">
              ⚠ For educational use only.<br>
              Not a financial advice.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return {
        "ticker":  selected_ticker,
        "name":    selected_name,
        "epochs":  epochs,
        "horizon": horizon,
        "run":     run,
    }
