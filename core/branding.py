"""
CryptoVision — core/branding.py
Loads and caches the app logo as a base64 data URI for use in inline HTML,
and exposes a filesystem path for st.set_page_config's page_icon.
"""

import base64
from pathlib import Path

import streamlit as st

LOGO_PATH = Path(__file__).resolve().parent.parent / "assets" / "LOGO.webp"


@st.cache_data(show_spinner=False)
def get_logo_data_uri() -> str:
    """Return the logo as a base64 data: URI, safe to drop into raw HTML."""
    with open(LOGO_PATH, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:image/webp;base64,{encoded}"