"""
CryptoVision — config/theme.py
"""

# Colour palette
PALETTE = {
    # Backgrounds — layered depth
    "bg_page":      "#0B0E11",   # deepest — page shell
    "bg_surface":   "#1E2026",   # primary card/panel surface
    "bg_elevated":  "#2B2F36",   # elevated elements, hover states
    "bg_input":     "#2B2F36",   # form inputs, dropdowns
    "bg_row_alt":   "#161A1E",   # alternating table rows

    "accent":       "#F0B90B",   # primary brand accent
    "accent_dim":   "#D4A109",   # darker accent for hover states
    "accent_glow":  "rgba(240,185,11,0.12)",  # subtle glow behind accent elements

    # Market colours — universal trading conventions
    "bull":         "#0ECB81",   # green — gains / bullish
    "bull_bg":      "rgba(14,203,129,0.08)",
    "bear":         "#F6465D",   # red — losses / bearish
    "bear_bg":      "rgba(246,70,93,0.08)",

    # Text hierarchy
    "text_primary": "#EAECEF",   # main content
    "text_secondary":"#848E9C",  # labels, secondary info
    "text_muted":   "#5E6673",   # placeholders, disabled
    "text_inverse": "#0B0E11",   # text on accent backgrounds

    # Structural
    "border":       "#2B2F36",
    "border_light": "#363C45",
    "divider":      "#1E2026",
}

# Chart styling
CHART_TEMPLATE  = "plotly_dark"
CHART_BG        = PALETTE["bg_surface"]
CHART_PAPER_BG  = PALETTE["bg_page"]
CHART_GRIDCOLOR = PALETTE["bg_elevated"]
CHART_FONT      = dict(
    family="'Barlow', 'DM Sans', sans-serif",
    color=PALETTE["text_secondary"],
    size=11,
)

# Global CSS
GLOBAL_CSS = f"""
<style>
  /* ── Fonts ──────────────────────────────────────────────────── */
  @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@600;700&family=DM+Mono:wght@400;500&display=swap');

  /* ── Hard resets ────────────────────────────────────────────── */
  *, *::before, *::after {{ box-sizing: border-box; }}

  html, body,
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  section.main,
  .main .block-container {{
      background-color: {PALETTE["bg_page"]} !important;
      color: {PALETTE["text_primary"]} !important;
      font-family: 'Barlow', sans-serif !important;
  }}

  /* ── Collapse header bar & remove top dead space ────────── */
  [data-testid="stHeader"] {{
      background-color: {PALETTE["bg_page"]} !important;
      height: 0 !important;
      min-height: 0 !important;
      overflow: hidden !important;
  }}

  [data-testid="stDecoration"] {{
      display: none !important;
  }}

  /* ── Remove top whitespace from the content column ─────── */
  .block-container {{
      padding-top: 0.75rem !important;
      padding-bottom: 3rem !important;
      max-width: 1200px !important;
  }}

  /* ── Sidebar collapse / expand arrow button ─────────────── */
  [data-testid="stSidebarCollapsedControl"] {{
      background-color: {PALETTE["bg_surface"]} !important;
      border: 1px solid {PALETTE["border_light"]} !important;
      border-radius: 0 4px 4px 0 !important;
  }}

  [data-testid="stSidebarCollapsedControl"] button {{
      background-color: transparent !important;
      color: {PALETTE["accent"]} !important;
  }}

  [data-testid="stSidebarCollapsedControl"] button:hover {{
      background-color: {PALETTE["bg_elevated"]} !important;
      color: {PALETTE["accent"]} !important;
  }}

  [data-testid="stSidebarCollapsedControl"] svg {{
      fill: {PALETTE["accent"]} !important;
      stroke: {PALETTE["accent"]} !important;
  }}

  /* ── Sidebar ────────────────────────────────────────────────── */
  [data-testid="stSidebar"],
  [data-testid="stSidebar"] > div:first-child {{
      background-color: {PALETTE["bg_surface"]} !important;
      border-right: 1px solid {PALETTE["border_light"]} !important;
  }}

  [data-testid="stSidebar"] * {{
      color: {PALETTE["text_primary"]} !important;
  }}

  [data-testid="stSidebarNav"] {{
      padding-top: 0 !important;
  }}

  /* ── Selectbox ──────────────────────────────────────────────── */
  [data-testid="stSelectbox"] > div > div,
  div[data-baseweb="select"] > div {{
      background-color: {PALETTE["bg_input"]} !important;
      border: 1px solid {PALETTE["border_light"]} !important;
      border-radius: 4px !important;
      color: {PALETTE["text_primary"]} !important;
      font-family: 'Barlow', sans-serif !important;
      font-size: 0.875rem !important;
  }}

  div[data-baseweb="select"] > div:hover {{
      border-color: {PALETTE["accent"]} !important;
  }}

  /* ── Sliders ────────────────────────────────────────────────── */
  [data-testid="stSlider"] > div > div > div > div {{
      background-color: {PALETTE["accent"]} !important;
  }}

  [data-testid="stSlider"] [data-testid="stThumbValue"] {{
      color: {PALETTE["accent"]} !important;
      font-family: 'DM Mono', monospace !important;
      font-size: 0.8rem !important;
  }}

  /* ── Primary button ─────────────────────────────────────────── */
  .stButton > button {{
      background-color: {PALETTE["accent"]} !important;
      color: {PALETTE["text_inverse"]} !important;
      border: none !important;
      border-radius: 4px !important;
      font-family: 'Barlow', sans-serif !important;
      font-weight: 700 !important;
      font-size: 0.875rem !important;
      letter-spacing: 0.04em !important;
      padding: 0.6rem 1.5rem !important;
      width: 100% !important;
      transition: background-color 0.15s ease !important;
      cursor: pointer !important;
  }}

  .stButton > button:hover {{
      background-color: {PALETTE["accent_dim"]} !important;
  }}

  /* ── Download button ────────────────────────────────────────── */
  [data-testid="stDownloadButton"] > button {{
      background-color: transparent !important;
      color: {PALETTE["accent"]} !important;
      border: 1px solid {PALETTE["accent"]} !important;
      border-radius: 4px !important;
      font-family: 'Barlow', sans-serif !important;
      font-weight: 600 !important;
      font-size: 0.82rem !important;
      letter-spacing: 0.03em !important;
      transition: all 0.15s ease !important;
  }}

  [data-testid="stDownloadButton"] > button:hover {{
      background-color: {PALETTE["accent_glow"]} !important;
  }}

  /* ── DataFrame ──────────────────────────────────────────────── */
  [data-testid="stDataFrame"] {{
      background-color: {PALETTE["bg_surface"]} !important;
      border: 1px solid {PALETTE["border_light"]} !important;
      border-radius: 6px !important;
      overflow: hidden;
  }}

  /* ── Expander ───────────────────────────────────────────────── */
  [data-testid="stExpander"] {{
      background-color: {PALETTE["bg_surface"]} !important;
      border: 1px solid {PALETTE["border_light"]} !important;
      border-radius: 6px !important;
  }}

  [data-testid="stExpander"] summary {{
      font-family: 'Barlow', sans-serif !important;
      font-weight: 600 !important;
      font-size: 0.85rem !important;
      color: {PALETTE["text_secondary"]} !important;
  }}

  /* ── Spinner ────────────────────────────────────────────────── */
  [data-testid="stSpinner"] > div {{
      border-top-color: {PALETTE["accent"]} !important;
  }}

  /* ── Alert / info boxes ─────────────────────────────────────── */
  [data-testid="stAlert"] {{
      background-color: {PALETTE["bg_elevated"]} !important;
      border-color: {PALETTE["border_light"]} !important;
      border-radius: 6px !important;
      color: {PALETTE["text_primary"]} !important;
  }}

  /* ── Progress bar ───────────────────────────────────────────── */
  [data-testid="stProgressBar"] > div > div {{
      background-color: {PALETTE["accent"]} !important;
  }}

  /* ── Hide Streamlit chrome ──────────────────────────────────── */
  #MainMenu, footer, [data-testid="stToolbar"] {{
      visibility: hidden !important;
  }}

  /* ── Scrollbar ──────────────────────────────────────────────── */
  ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
  ::-webkit-scrollbar-track {{ background: {PALETTE["bg_page"]}; }}
  ::-webkit-scrollbar-thumb {{
      background: {PALETTE["border_light"]};
      border-radius: 3px;
  }}
  ::-webkit-scrollbar-thumb:hover {{ background: {PALETTE["text_muted"]}; }}

  /* ── Headings ───────────────────────────────────────────────── */
  h1, h2, h3, h4 {{
      font-family: 'Barlow Condensed', sans-serif !important;
      color: {PALETTE["text_primary"]} !important;
      letter-spacing: 0.01em;
  }}

  /* ── Paragraph text ─────────────────────────────────────────── */
  p, li {{
      font-family: 'Barlow', sans-serif !important;
      color: {PALETTE["text_secondary"]} !important;
      font-size: 0.9rem !important;
      line-height: 1.65 !important;
  }}

  /* ── Sidebar labels (our custom labels) ─────────────────────── */
  .cv-sidebar-label {{
      font-family: 'Barlow Condensed', sans-serif;
      font-size: 0.68rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: {PALETTE["text_muted"]};
      margin-bottom: 4px;
      display: block;
  }}

  /* ── Stat pill ──────────────────────────────────────────────── */
  .cv-stat-pill {{
      display: inline-block;
      background: {PALETTE["bg_elevated"]};
      border: 1px solid {PALETTE["border_light"]};
      border-radius: 4px;
      padding: 2px 8px;
      font-family: 'DM Mono', monospace;
      font-size: 0.72rem;
      color: {PALETTE["text_secondary"]};
  }}
</style>
"""


def inject_theme() -> None:
    """Inject the global CSS into the active Streamlit page."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
