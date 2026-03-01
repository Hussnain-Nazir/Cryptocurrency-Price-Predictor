"""
CryptoVision — ui/views/predictor.py
Full prediction workflow: fetch → train → forecast → display.
"""

import pandas as pd
import numpy as np
import streamlit as st

from core.market_data import fetch_price_history, format_prediction_table
from core.forecast_engine import build_forecast, TRAIN_SPLIT_RATIO
from ui.components.charts import price_history_chart, forecast_chart, volume_chart, moving_average_chart, rsi_chart
from config.theme import PALETTE


# UI helpers
def _ticker_header(ticker: str, name: str) -> None:
    """Top bar with coin name"""
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: {PALETTE['bg_surface']};
            border: 1px solid {PALETTE['border_light']};
            border-radius: 4px;
            padding: 14px 20px;
            margin-bottom: 16px;
        ">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="
              width: 36px; height: 36px;
              background: {PALETTE['accent']};
              border-radius: 50%;
              display: flex; align-items: center; justify-content: center;
              font-family: 'Barlow Condensed', sans-serif;
              font-size: 0.72rem;
              font-weight: 700;
              color: {PALETTE['text_inverse']};
              flex-shrink: 0;
            ">{ticker.replace('-USD','')[:4]}</div>
            <div>
              <div style="
                font-family: 'Barlow Condensed', sans-serif;
                font-size: 1.1rem;
                font-weight: 700;
                color: {PALETTE['text_primary']};
                letter-spacing: 0.02em;
                line-height: 1.1;
              ">{ticker}</div>
              <div style="
                font-family: 'Barlow', sans-serif;
                font-size: 0.75rem;
                color: {PALETTE['text_muted']};
              ">{name}</div>
            </div>
          </div>
          <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: {PALETTE['text_muted']};
            background: {PALETTE['bg_elevated']};
            border: 1px solid {PALETTE['border_light']};
            border-radius: 3px;
            padding: 4px 10px;
          ">LSTM · DAILY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _stat_widget(label: str, value: str, change: str | None = None,
                 positive: bool | None = None) -> str:
    """Render a stat card as HTML string."""
    change_html = ""
    if change is not None:
        c_color = (
            PALETTE["bull"] if positive
            else PALETTE["bear"] if positive is False
            else PALETTE["text_muted"]
        )
        change_html = (
            f"<div style='font-family:DM Mono,monospace;font-size:0.72rem;"
            f"color:{c_color};margin-top:3px;'>{change}</div>"
        )
    return f"""
    <div style="
        background: {PALETTE['bg_surface']};
        border: 1px solid {PALETTE['border_light']};
        border-radius: 4px;
        padding: 14px 16px;
    ">
      <div style="
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {PALETTE['text_muted']};
        margin-bottom: 5px;
      ">{label}</div>
      <div style="
        font-family: 'Barlow Condensed', sans-serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: {PALETTE['text_primary']};
        letter-spacing: 0.01em;
        line-height: 1.1;
      ">{value}</div>
      {change_html}
    </div>
    """


def _section_bar(title: str) -> None:
    """Thin section divider with title."""
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 24px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid {PALETTE['border_light']};
        ">
          <div style="
            width: 3px; height: 14px;
            background: {PALETTE['accent']};
            border-radius: 2px;
          "></div>
          <div style="
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: {PALETTE['text_secondary']};
          ">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Main renderer
def render_predictor(controls: dict) -> None:
    ticker  = controls["ticker"]
    name    = controls["name"]
    epochs  = controls["epochs"]
    horizon = controls["horizon"]

    # Page header
    st.markdown(
        f"""
        <div style="margin-bottom: 4px;">
          <h1 style="
            font-family: 'Barlow Condensed', sans-serif !important;
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: {PALETTE['text_primary']} !important;
            letter-spacing: 0.02em;
            margin-bottom: 2px !important;
          ">Predictor</h1>
          <div style="
            font-family: 'Barlow', sans-serif;
            font-size: 0.75rem;
            color: {PALETTE['text_muted']};
          ">CryptoVision · LSTM Price Forecasting</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Coin header bar
    _ticker_header(ticker, name)

    # Fetch price history
    with st.spinner(f"Fetching price data for {ticker} …"):
        try:
            price_df, close_col = fetch_price_history(ticker)
        except ValueError as err:
            st.error(str(err))
            return

    close_series = price_df[close_col]

    # Market stats row
    _section_bar("Market Overview")

    latest      = close_series.iloc[-1]
    prev        = close_series.iloc[-2]
    day_chg     = latest - prev
    day_pct     = day_chg / prev * 100
    ath         = close_series.max()
    atl         = close_series.min()
    num_days    = len(close_series)
    is_positive = day_chg >= 0
    arrow       = "▲" if is_positive else "▼"

    stat_cols = st.columns(4)
    stats_data = [
        ("Last Close",     f"${latest:,.4f}",
         f"{arrow} {abs(day_pct):.2f}% (24h)", is_positive),
        ("All-Time High",  f"${ath:,.4f}",  None, None),
        ("All-Time Low",   f"${atl:,.6f}",  None, None),
        ("Trading Days",   f"{num_days:,}", None, None),
    ]
    for col, (lbl, val, chg, pos) in zip(stat_cols, stats_data):
        with col:
            st.markdown(_stat_widget(lbl, val, chg, pos), unsafe_allow_html=True)

    # Historical price chart
    _section_bar("Price History")

    fig_hist = price_history_chart(price_df.index, close_series, ticker)
    st.plotly_chart(fig_hist, use_container_width=True)

    # Volume chart (expandable)
    vol_col = next(
        (c for c in price_df.columns if "volume" in c.lower()), None
    )
    if vol_col:
        with st.expander("Trading Volume", expanded=False):
            fig_vol = volume_chart(
                price_df.index, price_df[vol_col], close_series, ticker
            )
            st.plotly_chart(fig_vol, use_container_width=True)

    # Technical Analysis (moved above LSTM Forecast)
    _section_bar("Technical Analysis")

    ta_tab_ma, ta_tab_rsi = st.tabs(["Moving Averages", "RSI"])

    with ta_tab_ma:
        fig_ma = moving_average_chart(
            dates=price_df.index,
            prices=close_series,
            ticker=ticker,
        )
        st.plotly_chart(fig_ma, use_container_width=True)
        st.markdown(
            f"""
            <div style="
                font-family: 'Barlow', sans-serif;
                font-size: 0.75rem;
                color: {PALETTE['text_muted']};
                padding: 4px 2px 12px 2px;
                line-height: 1.55;
            ">
              <b style="color:{PALETTE['text_secondary']};">MA20</b> — short-term trend (amber) &nbsp;|&nbsp;
              <b style="color:{PALETTE['text_secondary']};">MA50</b> — medium-term trend (green) &nbsp;|&nbsp;
              <b style="color:{PALETTE['text_secondary']};">MA200</b> — long-term trend (grey).
              A price crossing above its moving average is generally considered bullish.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with ta_tab_rsi:
        fig_rsi = rsi_chart(
            dates=price_df.index,
            prices=close_series,
            ticker=ticker,
        )
        st.plotly_chart(fig_rsi, use_container_width=True)
        st.markdown(
            f"""
            <div style="
                font-family: 'Barlow', sans-serif;
                font-size: 0.75rem;
                color: {PALETTE['text_muted']};
                padding: 4px 2px 12px 2px;
                line-height: 1.55;
            ">
              RSI above <b style="color:{PALETTE['bear']};">70</b> suggests the asset may be
              overbought. RSI below <b style="color:{PALETTE['bull']};">30</b> suggests it may be
              oversold. The midline at 50 separates bullish from bearish momentum.
              Calculated using a 14-day exponential moving average of gains and losses.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Training
    _section_bar("LSTM Forecast")

    progress = st.progress(0, text="Starting model training …")

    with st.spinner("Training the LSTM model — please wait …"):
        try:
            backtest_preds, future_preds = build_forecast(
                close_series.values,
                epochs=epochs,
                horizon_days=horizon,
            )
        except Exception as err:
            st.error(f"Model training failed: {err}")
            progress.empty()
            return

    progress.progress(100, text="Training complete ✓")

    # Align back-test dates
    split_idx      = int(len(close_series) * TRAIN_SPLIT_RATIO)
    backtest_dates = price_df.index[split_idx:]
    min_len        = min(len(backtest_dates), len(backtest_preds))
    backtest_dates = backtest_dates[-min_len:]
    backtest_preds = backtest_preds[-min_len:]

    # Future dates
    future_dates = pd.date_range(
        start=price_df.index[-1] + pd.Timedelta(days=1),
        periods=horizon,
    )

    # Forecast chart
    fig_fc = forecast_chart(
        hist_dates      = price_df.index,
        hist_prices     = close_series,
        backtest_dates  = backtest_dates,
        backtest_prices = backtest_preds,
        future_dates    = future_dates,
        future_prices   = future_preds,
        ticker          = ticker,
    )
    st.plotly_chart(fig_fc, use_container_width=True)

    # Forecast summary stats
    _section_bar("Forecast Summary")

    fc_start  = future_preds[0]
    fc_end    = future_preds[-1]
    fc_change = (fc_end - fc_start) / fc_start * 100
    fc_pos    = fc_change >= 0
    fc_arrow  = "▲" if fc_pos else "▼"

    fc_cols = st.columns(3)
    fc_stats = [
        ("Forecast Start",   f"${fc_start:,.6f}", None, None),
        ("Forecast End",     f"${fc_end:,.6f}",   None, None),
        ("Expected Change",
         f"{fc_arrow} {abs(fc_change):.2f}%",
         f"over {horizon} day{'s' if horizon != 1 else ''}",
         fc_pos),
    ]
    for col, (lbl, val, chg, pos) in zip(fc_cols, fc_stats):
        with col:
            st.markdown(_stat_widget(lbl, val, chg, pos), unsafe_allow_html=True)

    # Day-by-day table
    _section_bar("Day-by-Day Forecast")

    raw_table     = pd.DataFrame({"Date": future_dates, "Predicted Price": future_preds})
    display_table = format_prediction_table(raw_table)

    st.dataframe(
        display_table.style.format({"Forecast (USD)": "${:,.6f}"}),
        use_container_width=True,
        height=300,
    )

    # Download
    csv_data = display_table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Export Forecast as CSV",
        data=csv_data,
        file_name=f"{ticker}_forecast_{horizon}d.csv",
        mime="text/csv",
    )

    # Empty state cleanup
    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
