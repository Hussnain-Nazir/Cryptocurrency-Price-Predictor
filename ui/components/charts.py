"""
CryptoVision — ui/components/charts.py
Plotly figure builders styled after Binance's charting interface.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config.theme import (
    PALETTE, CHART_TEMPLATE, CHART_BG, CHART_PAPER_BG,
    CHART_GRIDCOLOR, CHART_FONT,
)


# Shared layout factory
def _base_layout(title_text: str = "", **overrides) -> dict:
    layout = dict(
        template=CHART_TEMPLATE,
        paper_bgcolor=CHART_PAPER_BG,
        plot_bgcolor=CHART_BG,
        font=CHART_FONT,
        margin=dict(l=16, r=16, t=44, b=36),
        title=dict(
            text=title_text,
            font=dict(
                family="'Barlow Condensed', sans-serif",
                size=13,
                color=PALETTE["text_secondary"],
            ),
            x=0.0,
            xanchor="left",
            pad=dict(l=4),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=PALETTE["border_light"],
            borderwidth=1,
            font=dict(size=11, color=PALETTE["text_secondary"]),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis=dict(
            gridcolor=CHART_GRIDCOLOR,
            linecolor=PALETTE["border_light"],
            tickfont=dict(size=10, color=PALETTE["text_muted"]),
            title_font=dict(size=10, color=PALETTE["text_muted"]),
            showgrid=True,
            zeroline=False,
            rangeslider=dict(visible=False),
        ),
        yaxis=dict(
            gridcolor=CHART_GRIDCOLOR,
            linecolor=PALETTE["border_light"],
            tickfont=dict(size=10, color=PALETTE["text_muted"]),
            title_font=dict(size=10, color=PALETTE["text_muted"]),
            showgrid=True,
            zeroline=False,
            tickprefix="$",
            side="right",
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor=PALETTE["bg_elevated"],
            bordercolor=PALETTE["border_light"],
            font=dict(
                family="'DM Mono', monospace",
                size=11,
                color=PALETTE["text_primary"],
            ),
        ),
    )
    layout.update(overrides)
    return layout


# Public figures
def price_history_chart(
    dates: pd.Index,
    prices: pd.Series,
    ticker: str,
) -> go.Figure:
    """
    Clean area chart of historical closing prices — Binance-style.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=prices,
            mode="lines",
            name="Close",
            line=dict(color=PALETTE["accent"], width=1.5),
            fill="tozeroy",
            fillcolor=PALETTE["accent_glow"],
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>$%{y:,.4f}<extra></extra>",
        )
    )

    fig.update_layout(
        **_base_layout(
            title_text=f"{ticker}  ·  Historical Close Price",
            xaxis_title="",
            yaxis_title="",
        )
    )
    return fig


def forecast_chart(
    hist_dates: pd.Index,
    hist_prices: pd.Series,
    backtest_dates: pd.Index,
    backtest_prices: np.ndarray,
    future_dates: pd.DatetimeIndex,
    future_prices: np.ndarray,
    ticker: str,
) -> go.Figure:
    """
    Three-trace overlay: historical · model fit · future forecast.
    """
    fig = go.Figure()

    # Historical baseline
    fig.add_trace(
        go.Scatter(
            x=hist_dates,
            y=hist_prices,
            mode="lines",
            name="Historical",
            line=dict(color=PALETTE["text_muted"], width=1.2),
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>$%{y:,.4f}<extra>Historical</extra>",
        )
    )

    # Model back-test fit
    fig.add_trace(
        go.Scatter(
            x=backtest_dates,
            y=backtest_prices,
            mode="lines",
            name="Model Fit",
            line=dict(color=PALETTE["bull"], width=1.4, dash="dot"),
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>$%{y:,.4f}<extra>Model Fit</extra>",
        )
    )

    # Future
    # Colour forecast line based on direction
    direction_color = (
        PALETTE["bull"] if future_prices[-1] >= future_prices[0]
        else PALETTE["bear"]
    )
    fill_color = (
        PALETTE["bull_bg"] if future_prices[-1] >= future_prices[0]
        else PALETTE["bear_bg"]
    )

    fig.add_trace(
        go.Scatter(
            x=future_dates,
            y=future_prices,
            mode="lines",
            name="Forecast",
            line=dict(color=direction_color, width=2),
            fill="tozeroy",
            fillcolor=fill_color,
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>$%{y:,.4f}<extra>Forecast</extra>",
        )
    )

    # Vertical separator at forecast start
    fig.add_vline(
        x=str(future_dates[0]),
        line=dict(color=PALETTE["border_light"], width=1, dash="dash"),
    )
    fig.add_annotation(
        x=str(future_dates[0]),
        y=0.98,
        yref="paper",
        text="Forecast Start",
        showarrow=False,
        font=dict(
            family="'DM Mono', monospace",
            size=9,
            color=PALETTE["text_muted"],
        ),
        xanchor="left",
        xshift=6,
    )

    fig.update_layout(
        **_base_layout(
            title_text=f"{ticker}  ·  Price Forecast",
        )
    )
    return fig


def volume_chart(
    dates: pd.Index,
    volumes: pd.Series,
    close_prices: pd.Series,
    ticker: str,
) -> go.Figure:
    """
    Volume bars using the app accent colour — consistent with other charts.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=dates,
            y=volumes,
            name="Volume",
            marker_color=PALETTE["accent"],
            marker_line_width=0,
            opacity=0.55,
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>Vol: %{y:,.0f}<extra></extra>",
        )
    )

    fig.update_layout(
        **_base_layout(
            title_text=f"{ticker}  ·  Trading Volume",
            yaxis=dict(
                gridcolor=CHART_GRIDCOLOR,
                linecolor=PALETTE["border_light"],
                tickfont=dict(size=10, color=PALETTE["text_muted"]),
                title_font=dict(size=10, color=PALETTE["text_muted"]),
                showgrid=True,
                zeroline=False,
                tickprefix="",
                side="right",
            ),
        )
    )
    return fig


def moving_average_chart(
    dates: pd.Index,
    prices: pd.Series,
    ticker: str,
    windows: tuple[int, ...] = (20, 50, 200),
) -> go.Figure:
    """
    Closing price overlaid with Simple Moving Average lines.
    windows: tuple of MA periods to plot, e.g. (20, 50, 200).
    """
    # MA line colours
    ma_colors = [PALETTE["accent"], PALETTE["bull"], PALETTE["text_secondary"]]

    fig = go.Figure()

    # Raw close price (faint baseline)
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=prices,
            mode="lines",
            name="Close",
            line=dict(color=PALETTE["text_muted"], width=1),
            opacity=0.5,
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>$%{y:,.4f}<extra>Close</extra>",
        )
    )

    # One trace per MA window
    for idx, window in enumerate(windows):
        if len(prices) < window:
            # Skip if not enough data for this window
            continue
        ma_series = prices.rolling(window=window).mean()
        color = ma_colors[idx % len(ma_colors)]
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=ma_series,
                mode="lines",
                name=f"MA {window}",
                line=dict(color=color, width=1.6),
                hovertemplate=f"<b>%{{x|%b %d, %Y}}</b><br>MA{window}: $%{{y:,.4f}}<extra>MA {window}</extra>",
            )
        )

    fig.update_layout(
        **_base_layout(
            title_text=f"{ticker}  ·  Moving Averages  (MA20 / MA50 / MA200)",
        )
    )
    return fig


def rsi_chart(
    dates: pd.Index,
    prices: pd.Series,
    ticker: str,
    period: int = 14,
) -> go.Figure:
    """
    Relative Strength Index (RSI) chart with overbought/oversold reference bands.
    period: RSI lookback window (standard = 14 days).
    """
    # Calculate RSI
    delta = prices.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs  = avg_gain / avg_loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))

    fig = go.Figure()

    # Reference bands
    # Overbought shading (70–100)
    fig.add_hrect(
        y0=70, y1=100,
        fillcolor=PALETTE["bear_bg"],
        line_width=0,
        annotation_text="Overbought",
        annotation_position="top right",
        annotation_font=dict(
            family="'DM Mono', monospace",
            size=9,
            color=PALETTE["bear"],
        ),
    )

    # Oversold shading (0–30)
    fig.add_hrect(
        y0=0, y1=30,
        fillcolor=PALETTE["bull_bg"],
        line_width=0,
        annotation_text="Oversold",
        annotation_position="bottom right",
        annotation_font=dict(
            family="'DM Mono', monospace",
            size=9,
            color=PALETTE["bull"],
        ),
    )

    # Overbought line at 70
    fig.add_hline(
        y=70,
        line=dict(color=PALETTE["bear"], width=1, dash="dot"),
    )

    # Oversold line at 30
    fig.add_hline(
        y=30,
        line=dict(color=PALETTE["bull"], width=1, dash="dot"),
    )

    # Midline at 50
    fig.add_hline(
        y=50,
        line=dict(color=PALETTE["border_light"], width=1, dash="dash"),
    )

    # RSI line
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=rsi,
            mode="lines",
            name=f"RSI ({period})",
            line=dict(color=PALETTE["accent"], width=1.8),
            hovertemplate="<b>%{x|%b %d, %Y}</b><br>RSI: %{y:.1f}<extra></extra>",
        )
    )

    fig.update_layout(
        **_base_layout(
            title_text=f"{ticker}  ·  RSI ({period}-day)",
            yaxis=dict(
                gridcolor=CHART_GRIDCOLOR,
                linecolor=PALETTE["border_light"],
                tickfont=dict(size=10, color=PALETTE["text_muted"]),
                title_font=dict(size=10, color=PALETTE["text_muted"]),
                showgrid=True,
                zeroline=False,
                tickprefix="",
                range=[0, 100],
                side="right",
            ),
        )
    )
    return fig
