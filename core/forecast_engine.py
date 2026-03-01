"""
CryptoVision — core/forecast_engine.py
Builds, trains, and runs an LSTM-based price forecasting model.
"""

from __future__ import annotations

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense


# Configuration
LOOKBACK_WINDOW   = 60     # days of history fed to each training sample
TRAIN_SPLIT_RATIO = 0.80   # fraction of data used for training
LSTM_UNITS        = 50     # neurons per LSTM layer
DENSE_HIDDEN      = 25     # neurons in the intermediate Dense layer
BATCH_SIZE        = 1


# Public API
def build_forecast(
    price_series: np.ndarray,
    epochs: int,
    horizon_days: int,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Train a two-layer LSTM on *price_series* and predict *horizon_days* ahead.

    Parameters
    ----------
    price_series  : 1-D array of closing prices (chronological order)
    epochs        : training iterations
    horizon_days  : number of future days to forecast

    Returns
    -------
    test_predictions  : back-tested predictions aligned with the test split
    future_predictions: forecasted prices for the next *horizon_days* days
    """
    scaler, scaled = _scale(price_series)
    split_idx       = int(len(scaled) * TRAIN_SPLIT_RATIO)

    # Training data
    X_train, y_train = _make_sequences(scaled[:split_idx])
    X_train = _reshape(X_train)

    # Model
    model = _compile_model(X_train.shape[1])
    model.fit(X_train, y_train, batch_size=BATCH_SIZE, epochs=epochs, verbose=0)

    # Back-test predictions
    test_input        = scaled[split_idx - LOOKBACK_WINDOW:]
    X_test, _         = _make_sequences(test_input)
    test_preds_scaled = model.predict(_reshape(X_test), verbose=0)
    test_predictions  = scaler.inverse_transform(test_preds_scaled).flatten()

    # Future forecast
    rolling_window  = scaled[-LOOKBACK_WINDOW:].copy()
    future_scaled   = []

    for _ in range(horizon_days):
        x_in       = rolling_window.reshape(1, LOOKBACK_WINDOW, 1)
        next_step  = model.predict(x_in, verbose=0)[0, 0]
        future_scaled.append(next_step)
        rolling_window = np.append(rolling_window[1:], [[next_step]], axis=0)

    future_predictions = scaler.inverse_transform(
        np.array(future_scaled).reshape(-1, 1)
    ).flatten()

    return test_predictions, future_predictions


# Private helpers
def _scale(series: np.ndarray) -> tuple[MinMaxScaler, np.ndarray]:
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(series.reshape(-1, 1))
    return scaler, scaled


def _make_sequences(
    data: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Slide a window of size LOOKBACK_WINDOW over *data* to produce (X, y) pairs."""
    X, y = [], []
    for i in range(LOOKBACK_WINDOW, len(data)):
        X.append(data[i - LOOKBACK_WINDOW : i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)


def _reshape(X: np.ndarray) -> np.ndarray:
    """Add the feature dimension required by Keras LSTM: (samples, timesteps, 1)."""
    return X.reshape(X.shape[0], X.shape[1], 1)


def _compile_model(timesteps: int) -> Sequential:
    model = Sequential(
        [
            LSTM(LSTM_UNITS, return_sequences=True, input_shape=(timesteps, 1)),
            LSTM(LSTM_UNITS, return_sequences=False),
            Dense(DENSE_HIDDEN, activation="relu"),
            Dense(1),
        ]
    )
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model
