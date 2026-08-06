"""
CryptoVision — HOME.py
Main Streamlit entry-point. Renders the Home page.

Run with:
    streamlit run HOME.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from config.theme import inject_theme
from ui.views.home import render_home
from core.branding import LOGO_PATH

st.set_page_config(
    page_title="CryptoVision – Cryptocurrency Price Predictor",
    page_icon=str(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()
render_home()
