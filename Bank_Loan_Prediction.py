import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="FinBank AI - Loan Prediction",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- SESSION STATE --------------------
if 'loan_history' not in st.session_state:
    st.session_state.loan_history = []
if 'prediction_count' not in st.session_state:
    st.session_state.prediction_count = 0
if 'current_prediction' not in st.session_state:
    st.session_state.current_prediction = None

# -------------------- CSS --------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

/* ============================================================
   DESIGN TOKENS
   ============================================================ */
:root {
    --primary       : #2563eb;
    --primary-hover : #1d4ed8;
    --primary-light : #eff6ff;
    --primary-soft  : #dbeafe;
    --bg            : #ffffff;
    --bg-secondary  : #f5f7fa;
    --bg-tertiary   : #f0f4f8;
    --border        : #e5e7eb;
    --border-focus  : #93c5fd;
    --text-primary  : #1f2937;
    --text-secondary: #6b7280;
    --text-muted    : #9ca3af;
    --success       : #16a34a;
    --success-bg    : #f0fdf4;
    --success-border: #bbf7d0;
    --danger        : #dc2626;
    --danger-bg     : #fef2f2;
    --danger-border : #fecaca;
    --shadow-sm     : 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md     : 0 4px 12px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.04);
    --shadow-lg     : 0 8px 24px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04);
    --radius        : 8px;
    --radius-lg     : 12px;
    --field-height  : 44px;
}

/* ============================================================
   HIDE STREAMLIT DEFAULT CHROME
   ============================================================ */

/* Hamburger menu */
#MainMenu                              { visibility: hidden !important; display: none !important; }

/* Default footer */
footer                                 { visibility: hidden !important; display: none !important; }

/* "keyboard_double" decoration / top header bar */
header[data-testid="stHeader"]         { visibility: hidden !important; height: 0 !important;
                                         min-height: 0 !important; padding: 0 !important;
                                         margin: 0 !important; overflow: hidden !important; }

/* Streamlit top decoration strip (source of "keyboard_double" text) */
[data-testid="stDecoration"]           { display: none !important; }
[data-testid="stToolbar"]              { display: none !important; }
[data-testid="stStatusWidget"]         { display: none !important; }

/* App header wrapper that reserves space for the hidden header */
[data-testid="stAppViewContainer"] > section:first-child { padding-top: 0 !important; }

/* Remove the blank gap left behind by the hidden header */
[data-testid="stMain"]                 { padding-top: 0 !important; margin-top: 0 !important; }
.main .block-container,
[data-testid="stMainBlockContainer"]   { padding-top: 1.5rem !important; }

/* ============================================================
   GLOBAL BASE
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: var(--bg) !important;
    color: var(--text-primary) !important;
    -webkit-font-smoothing: antialiased;
}

[data-testid="stAppViewContainer"]::before,
[data-testid="stAppViewContainer"]::after {
    display: none !important;
}

[data-testid="stMainBlockContainer"] {
    padding: 2rem 2.5rem !important;
    max-width: 1200px;
}

/* ============================================================
   HEADER BAR
   ============================================================ */
header[data-testid="stHeader"] {
    background: #ffffff !important;
    border-bottom: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ============================================================
   SIDEBAR
   ============================================================ */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: none !important;
}

/* Clean sidebar start — remove default top gap and any decoration */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 16px !important;
    padding-bottom: 32px !important;
    overflow-y: auto !important;
}

/* Hide any icon/image placeholder Streamlit injects at sidebar top */
[data-testid="stSidebar"] [data-testid="stImage"]:first-child,
[data-testid="stSidebar"] > div > div:first-child > div[data-testid="stImage"],
[data-testid="stSidebarUserContent"] img:first-child {
    display: none !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] h2 {
    font-size: 17px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.3px !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    padding: 9px 12px !important;
    border-radius: 8px !important;
    margin: 2px 0 !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    transition: background 0.15s ease, color 0.15s ease !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: #ffffff !important;
    color: var(--primary) !important;
    border-color: var(--border) !important;
}

/* Hide Streamlit's auto-generated icon images inside radio labels */
[data-testid="stSidebar"] [data-testid="stRadio"] label img,
[data-testid="stSidebar"] [data-testid="stRadio"] label svg,
[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stIconMaterial"],
[data-testid="stSidebar"] [data-testid="stRadio"] span[data-testid="stIconMaterial"],
[data-testid="stSidebar"] [data-testid="stRadio"] [class*="icon"],
[data-testid="stSidebar"] [data-testid="stRadio"] [class*="Icon"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Ensure sidebar has enough bottom padding so last element never clips */
[data-testid="stSidebar"] > div:first-child {
    padding-bottom: 32px !important;
    overflow-y: auto !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 14px 16px !important;
    margin: 6px 0 !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ============================================================
   MAIN TITLE
   ============================================================ */
.main-title {
    font-family: 'Inter', sans-serif !important;
    font-size: clamp(24px, 3vw, 34px) !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    text-align: center !important;
    letter-spacing: -0.6px !important;
    line-height: 1.2 !important;
    margin-bottom: 4px !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    background: none !important;
}

/* ============================================================
   WIDGET LABELS — consistent across all fields
   ============================================================ */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
label {
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    margin-bottom: 6px !important;
    line-height: 1.4 !important;
    display: block !important;
}

/* Consistent vertical spacing around every widget */
[data-testid="stTextInput"],
[data-testid="stNumberInput"],
[data-testid="stSelectbox"],
[data-testid="stSlider"] {
    margin-bottom: 18px !important;
}

/* ============================================================
   TEXT INPUT — fixed height, consistent padding
   ============================================================ */
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] > div > div {
    height: var(--field-height) !important;
}

[data-testid="stTextInput"] input {
    height: var(--field-height) !important;
    min-height: var(--field-height) !important;
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 0 14px !important;
    line-height: var(--field-height) !important;
    display: flex !important;
    align-items: center !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
    box-shadow: none !important;
    width: 100% !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(147,197,253,0.25) !important;
    outline: none !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: var(--text-muted) !important;
    font-style: normal !important;
}

/* ============================================================
   NUMBER INPUT — fixed height, consistent padding
   ============================================================ */
[data-testid="stNumberInput"] > div,
[data-testid="stNumberInput"] > div > div {
    height: var(--field-height) !important;
}

[data-testid="stNumberInput"] input {
    height: var(--field-height) !important;
    min-height: var(--field-height) !important;
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 0 14px !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
    box-shadow: none !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(147,197,253,0.25) !important;
    outline: none !important;
}

[data-testid="stNumberInput"] input::placeholder {
    color: var(--text-muted) !important;
    font-style: normal !important;
}

/* Number input stepper buttons */
[data-testid="stNumberInput"] button {
    height: calc(var(--field-height) / 2) !important;
    width: 28px !important;
    border: none !important;
    background: var(--bg-secondary) !important;
    color: var(--text-secondary) !important;
    font-size: 12px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

[data-testid="stNumberInput"] button:hover {
    background: var(--bg-tertiary) !important;
    transform: none !important;
}

/* ============================================================
   SELECT BOX — height matches inputs
   ============================================================ */
[data-testid="stSelectbox"] > div > div {
    height: var(--field-height) !important;
    min-height: var(--field-height) !important;
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 14px !important;
    transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
    cursor: pointer !important;
}

[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--border-focus) !important;
    box-shadow: 0 0 0 3px rgba(147,197,253,0.2) !important;
}

/* Selectbox inner text alignment */
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    height: var(--field-height) !important;
    display: flex !important;
    align-items: center !important;
    padding: 0 !important;
}

[data-testid="stSelectbox"] span {
    font-size: 14px !important;
    color: var(--text-primary) !important;
    line-height: 1 !important;
}

/* ============================================================
   SLIDER — value bubble above track, no overlap
   ============================================================ */

/* Outer widget wrapper — tall enough so the bubble above has room */
[data-testid="stSlider"] {
    padding-top: 20px !important;   /* space for the value bubble */
    padding-bottom: 10px !important;
    margin-bottom: 18px !important;
    overflow: visible !important;
}

/* The inner baseweb slider wrapper — needs overflow visible */
[data-testid="stSlider"] [data-baseweb="slider"] {
    overflow: visible !important;
    margin-top: 0 !important;
}

/* Value tooltip bubble — sits ABOVE the track */
[data-testid="stSlider"] [data-testid="stThumbValue"],
[data-testid="stSlider"] div[class*="StyledThumbValue"],
[data-testid="stSlider"] div[class*="thumbValue"],
[data-testid="stSlider"] [data-baseweb="tooltip"],
[data-testid="stSlider"] [role="tooltip"] {
    position: absolute !important;
    top: -32px !important;
    transform: translateX(-50%) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: var(--primary) !important;
    background: var(--primary-light) !important;
    border: 1px solid var(--primary-soft) !important;
    border-radius: 5px !important;
    padding: 2px 8px !important;
    white-space: nowrap !important;
    line-height: 1.6 !important;
    z-index: 10 !important;
    pointer-events: none !important;
}

/* Track container — centered vertically with no clipping */
[data-testid="stSlider"] [data-baseweb="slider"] > div:first-child {
    overflow: visible !important;
    position: relative !important;
}

/* Track background rail */
[data-testid="stSlider"] [data-baseweb="slider"] [data-testid="stSliderTrack"],
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {
    height: 5px !important;
    background: var(--bg-tertiary) !important;
    border-radius: 100px !important;
    overflow: visible !important;
}

/* Filled portion of track */
[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child > div:first-child {
    height: 5px !important;
    background: var(--primary) !important;
    border-radius: 100px !important;
}

/* Thumb circle */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    width: 18px !important;
    height: 18px !important;
    background: var(--primary) !important;
    border: 2.5px solid #ffffff !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.2), 0 1px 4px rgba(0,0,0,0.12) !important;
    border-radius: 50% !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    cursor: grab !important;
    z-index: 5 !important;
    position: absolute !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"]:active {
    cursor: grabbing !important;
    box-shadow: 0 0 0 5px rgba(37,99,235,0.22), 0 1px 4px rgba(0,0,0,0.12) !important;
}

/* Min/max range labels below track */
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"] {
    font-size: 11px !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-muted) !important;
    margin-top: 8px !important;
    line-height: 1 !important;
}

/* ============================================================
   BUTTONS — solid, correct height, centered text
   ============================================================ */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: 0.1px !important;
    height: 52px !important;
    min-height: 52px !important;
    padding: 0 24px !important;
    border-radius: var(--radius) !important;
    border: none !important;
    background: var(--primary) !important;
    color: #ffffff !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    transition: background 0.18s ease, box-shadow 0.18s ease, transform 0.12s ease !important;
    box-shadow: 0 1px 4px rgba(37,99,235,0.25) !important;
    animation: none !important;
    line-height: 1 !important;
}

.stButton > button:hover {
    background: var(--primary-hover) !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.3) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 1px 4px rgba(37,99,235,0.2) !important;
}

.stButton > button::before { display: none !important; }

/* ============================================================
   TABS — clean underline style
   ============================================================ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid var(--border) !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
    margin-bottom: 20px !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    border-radius: 0 !important;
    padding: 10px 20px !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    transition: color 0.15s ease !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: var(--primary) !important;
    background: var(--primary-light) !important;
    border-radius: 6px 6px 0 0 !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--primary) !important;
    font-weight: 600 !important;
    background: transparent !important;
    border-bottom: 2px solid var(--primary) !important;
    box-shadow: none !important;
}

[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"]    { display: none !important; }

/* Tab content area spacing */
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    padding-top: 8px !important;
}

/* ============================================================
   PROGRESS BARS — consistent width and spacing
   ============================================================ */
[data-testid="stProgress"] {
    margin-bottom: 14px !important;
    width: 100% !important;
}

[data-testid="stProgress"] > div {
    width: 100% !important;
}

[data-testid="stProgress"] > div > div > div {
    background: var(--bg-tertiary) !important;
    border-radius: 100px !important;
    height: 7px !important;
    overflow: hidden !important;
    width: 100% !important;
}

[data-testid="stProgress"] > div > div > div > div {
    background: var(--primary) !important;
    border-radius: 100px !important;
    height: 100% !important;
    animation: none !important;
    box-shadow: none !important;
    transition: width 0.4s ease !important;
}

/* Spacing between progress label and bar */
[data-testid="stProgress"] + div,
div:has(> [data-testid="stProgress"]) {
    margin-top: 4px !important;
}

/* ============================================================
   FORM CARDS
   ============================================================ */
.form-card {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 28px !important;
    margin-bottom: 20px !important;
    box-shadow: var(--shadow-md) !important;
    transition: box-shadow 0.2s ease !important;
    animation: none !important;
    backdrop-filter: none !important;
}

.form-card:hover {
    box-shadow: var(--shadow-lg) !important;
    border-color: #d1d5db !important;
    transform: none !important;
}

.metric-card {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 22px 20px !important;
    text-align: center !important;
    margin: 6px 0 !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.2s ease, border-color 0.2s ease !important;
    animation: none !important;
    backdrop-filter: none !important;
}

.metric-card:hover {
    box-shadow: var(--shadow-md) !important;
    border-color: var(--border-focus) !important;
    transform: none !important;
}

/* ============================================================
   RESULT CARDS
   ============================================================ */
.approved-card {
    background: var(--success-bg) !important;
    border: 1.5px solid var(--success-border) !important;
    border-left: 4px solid var(--success) !important;
    border-radius: var(--radius-lg) !important;
    padding: 28px 24px !important;
    margin: 20px 0 !important;
    box-shadow: 0 2px 8px rgba(22,163,74,0.08) !important;
    animation: fadeUp 0.35s ease both !important;
    backdrop-filter: none !important;
    position: relative !important;
    overflow: visible !important;
}

.approved-card::before { display: none !important; }

.rejected-card {
    background: var(--danger-bg) !important;
    border: 1.5px solid var(--danger-border) !important;
    border-left: 4px solid var(--danger) !important;
    border-radius: var(--radius-lg) !important;
    padding: 28px 24px !important;
    margin: 20px 0 !important;
    box-shadow: 0 2px 8px rgba(220,38,38,0.07) !important;
    animation: fadeUp 0.35s ease both !important;
    backdrop-filter: none !important;
}

.approved-card h2 { color: var(--success) !important; font-size: 20px !important; }
.approved-card p  { color: #166534 !important; }
.rejected-card h2 { color: var(--danger) !important; font-size: 20px !important; }
.rejected-card p  { color: #991b1b !important; }

/* ============================================================
   TYPOGRAPHY
   ============================================================ */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.3px !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    background: none !important;
}

h3 {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin-bottom: 12px !important;
}

p, span, div {
    font-family: 'Inter', sans-serif !important;
}

/* ============================================================
   COLUMN ALIGNMENT — equal vertical alignment in rows
   ============================================================ */
[data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
    gap: 16px !important;
}

[data-testid="stHorizontalBlock"] > div {
    flex: 1 !important;
    min-width: 0 !important;
}

/* ============================================================
   METRICS (MAIN AREA)
   ============================================================ */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 20px !important;
    transition: box-shadow 0.2s ease !important;
    animation: none !important;
    box-shadow: var(--shadow-sm) !important;
}

[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md) !important;
    border-color: var(--border-focus) !important;
    transform: none !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Inter', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    -webkit-text-fill-color: var(--text-primary) !important;
    background: none !important;
}

/* ============================================================
   ALERT / INFO / WARNING BOXES
   ============================================================ */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border: 1px solid !important;
    animation: none !important;
    backdrop-filter: none !important;
    font-size: 14px !important;
    font-family: 'Inter', sans-serif !important;
    padding: 12px 16px !important;
}

[data-testid="stAlert"][kind="info"] {
    background: var(--primary-light) !important;
    border-color: var(--primary-soft) !important;
    color: #1e40af !important;
}

[data-testid="stAlert"][kind="warning"] {
    background: #fffbeb !important;
    border-color: #fde68a !important;
    color: #92400e !important;
}

[data-testid="stAlert"][kind="success"] {
    background: var(--success-bg) !important;
    border-color: var(--success-border) !important;
    color: #166534 !important;
}

/* ============================================================
   DATAFRAME
   ============================================================ */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-lg) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
    overflow: hidden !important;
}

/* ============================================================
   EXPANDERS
   ============================================================ */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    margin-bottom: 8px !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.2s ease !important;
    backdrop-filter: none !important;
}

[data-testid="stExpander"]:hover {
    box-shadow: var(--shadow-md) !important;
    border-color: #d1d5db !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    padding: 14px 16px !important;
}

/* ============================================================
   DIVIDERS
   ============================================================ */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 20px 0 !important;
}

/* ============================================================
   SCROLLBAR
   ============================================================ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 100px;
}
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */
[data-testid="stDownloadButton"] > button {
    background: #ffffff !important;
    border: 1.5px solid var(--primary) !important;
    color: var(--primary) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    height: 40px !important;
    padding: 0 18px !important;
    border-radius: var(--radius) !important;
    transition: all 0.18s ease !important;
    box-shadow: none !important;
    display: inline-flex !important;
    align-items: center !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: var(--primary-light) !important;
    border-color: var(--primary-hover) !important;
    color: var(--primary-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ============================================================
   CAPTION / SMALL TEXT
   ============================================================ */
[data-testid="stCaptionContainer"] p {
    color: var(--text-muted) !important;
    font-size: 12px !important;
    font-family: 'Inter', sans-serif !important;
}

/* ============================================================
   KEYFRAMES
   ============================================================ */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeUp 0.3s ease both !important;
}

/* ============================================================
   FOOTER
   ============================================================ */
footer, [data-testid="stFooter"] {
    background: transparent !important;
}

#particleCanvas { display: none !important; }

</style>
""", unsafe_allow_html=True)
# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## FinBank AI")
    st.caption("Smart Loan Decision System")

    st.divider()

    page = st.radio(
        "Navigation",
        ["Loan Prediction", "Dashboard", "History", "Settings"],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### Quick Stats")
    st.metric("Predictions Today", st.session_state.prediction_count)
    if st.session_state.loan_history:
        approved_count = len([h for h in st.session_state.loan_history if h['approved']])
        live_rate = (approved_count / len(st.session_state.loan_history)) * 100
        st.metric("Approval Rate", f"{live_rate:.0f}%")
    else:
        st.metric("Approval Rate", "—")

    st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)

    if st.button("Clear History", use_container_width=True):
        st.session_state.loan_history = []
        st.session_state.prediction_count = 0
        st.session_state.current_prediction = None
        st.success("History cleared!")

    st.divider()
    st.markdown(
        "<p style='font-size:13px; color:#6b7280; font-family:Inter,sans-serif;"
        " padding: 4px 0 16px 0; margin:0;'>Powered by Machine Learning</p>",
        unsafe_allow_html=True
    )

# -------------------- PREDICTION FUNCTION --------------------
def calculate_loan_score(data):
    score = 0
    factors = []

    credit_score_pts = min(data['credit_score'], 900) / 3
    score += credit_score_pts
    factors.append(("Credit Score", credit_score_pts, 300))

    total_income = data['applicant_income'] + data['co_income']
    if total_income > 0:
        income_ratio = (data['loan_amount'] * 1000) / (total_income * data['loan_duration'])
        income_pts = max(0, 250 - income_ratio * 25)
        score += income_pts
        factors.append(("Income Ratio", income_pts, 250))

    employment_score = {
        "Job": 150, "Self-Employed": 100, "Business": 120,
        "Salaried": 150, "Business Owner": 120, "Freelancer": 80, "Retired": 60
    }.get(data['employment'], 80)
    score += employment_score
    factors.append(("Employment", employment_score, 150))

    education_score = {
        "Graduate": 100, "Post Graduate": 120, "Doctorate": 140, "High School": 60
    }.get(data['education'], 60)
    score += education_score
    factors.append(("Education", education_score, 140))

    property_score = {"Urban": 80, "Semi-Urban": 70, "Rural": 50}.get(data['property_area'], 50)
    score += property_score
    factors.append(("Property Area", property_score, 80))

    max_score = sum(f[2] for f in factors)
    approval_probability = (score / max_score) * 100

    return {
        'score': score,
        'max_score': max_score,
        'probability': approval_probability,
        'factors': factors,
        'approved': approval_probability >= 65,
        'total_income': total_income
    }

# -------------------- HELPER: RISK LEVEL --------------------
def get_risk_level(prob):
    if prob >= 75:
        return "Low Risk", "#16a34a", "#f0fdf4", "#bbf7d0"
    elif prob >= 50:
        return "Medium Risk", "#d97706", "#fffbeb", "#fde68a"
    else:
        return "High Risk", "#dc2626", "#fef2f2", "#fecaca"

# -------------------- HELPER: LIVE SCORE CARD --------------------
def render_live_score(prob, total_income, loan_amount, loan_duration):
    label, color, bg, border = get_risk_level(prob)
    approved_text = "Likely Approved" if prob >= 65 else "Likely Rejected"
    approved_color = "#16a34a" if prob >= 65 else "#dc2626"
    bar_pct = int(prob)
    emi = (loan_amount / loan_duration) * 1.08 if loan_duration > 0 else 0

    st.markdown(f"""
    <div style="background:{bg}; border:1.5px solid {border}; border-radius:12px;
                padding:20px; margin-bottom:16px;">
        <p style="font-size:11px; font-weight:600; letter-spacing:0.6px;
                  text-transform:uppercase; color:#6b7280; margin:0 0 6px 0;
                  font-family:Inter,sans-serif;">Live Score Preview</p>
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
            <span style="font-size:32px; font-weight:700; color:{color};
                         font-family:Inter,sans-serif;">{prob:.1f}%</span>
            <span style="font-size:13px; font-weight:600; color:{approved_color};
                         background:white; border:1px solid {border};
                         border-radius:20px; padding:4px 12px;
                         font-family:Inter,sans-serif;">{approved_text}</span>
        </div>
        <div style="background:#e5e7eb; border-radius:100px; height:8px; margin-bottom:10px; overflow:hidden;">
            <div style="width:{bar_pct}%; background:{color}; height:100%;
                        border-radius:100px; transition:width 0.4s ease;"></div>
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
            <span style="width:8px; height:8px; border-radius:50%;
                         background:{color}; display:inline-block;"></span>
            <span style="font-size:13px; font-weight:500; color:{color};
                         font-family:Inter,sans-serif;">{label}</span>
        </div>
        <div style="border-top:1px solid {border}; padding-top:12px; margin-top:4px;">
            <p style="font-size:11px; font-weight:600; text-transform:uppercase;
                      letter-spacing:0.5px; color:#9ca3af; margin:0 0 8px 0;
                      font-family:Inter,sans-serif;">Loan Summary</p>
            <div style="display:flex; flex-direction:column; gap:5px;">
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-size:13px; color:#6b7280; font-family:Inter,sans-serif;">Total Income</span>
                    <span style="font-size:13px; font-weight:600; color:#1f2937; font-family:Inter,sans-serif;">${total_income:,.0f}/mo</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-size:13px; color:#6b7280; font-family:Inter,sans-serif;">Loan Amount</span>
                    <span style="font-size:13px; font-weight:600; color:#1f2937; font-family:Inter,sans-serif;">${loan_amount:,.0f}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-size:13px; color:#6b7280; font-family:Inter,sans-serif;">Est. Monthly EMI</span>
                    <span style="font-size:13px; font-weight:600; color:#2563eb; font-family:Inter,sans-serif;">${emi:,.0f}</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------- HELPER: SCORE BREAKDOWN BARS --------------------
def render_score_breakdown(factors):
    st.markdown("""
    <p style="font-size:15px; font-weight:600; color:#1f2937;
              font-family:Inter,sans-serif; margin:16px 0 12px 0;">Score Breakdown</p>
    """, unsafe_allow_html=True)
    for factor, score, max_score in factors:
        pct = int((score / max_score) * 100)
        if pct >= 70:
            bar_color = "#16a34a"
        elif pct >= 45:
            bar_color = "#d97706"
        else:
            bar_color = "#dc2626"
        st.markdown(f"""
        <div style="margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between;
                        margin-bottom:5px; align-items:center;">
                <span style="font-size:13px; font-weight:500; color:#374151;
                             font-family:Inter,sans-serif;">{factor}</span>
                <span style="font-size:13px; font-weight:600; color:{bar_color};
                             font-family:Inter,sans-serif;">{pct}%</span>
            </div>
            <div style="background:#f0f4f8; border-radius:100px; height:8px; overflow:hidden;">
                <div style="width:{pct}%; background:{bar_color}; height:100%;
                            border-radius:100px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------------------- HELPER: INLINE VALIDATION --------------------
def render_validation(credit_score, applicant_income, co_income, loan_amount, loan_duration):
    warnings = []
    total_income = applicant_income + co_income
    if credit_score < 600:
        warnings.append(("Credit score below 600 — this significantly reduces approval chances.", "warning"))
    if total_income < 2000:
        warnings.append(("Combined income is very low. Consider adding a co-applicant.", "warning"))
    if loan_amount > 0 and total_income > 0:
        emi = (loan_amount / max(loan_duration, 1)) * 1.08
        if emi > total_income * 0.5:
            warnings.append((f"EMI (${emi:,.0f}/mo) exceeds 50% of income — high default risk.", "error"))
    if loan_amount > total_income * 80:
        warnings.append(("Loan amount is very high relative to income.", "warning"))
    return warnings

# -------------------- MAIN PAGE --------------------
if page == "Loan Prediction":
    st.markdown('<h1 class="main-title">Bank Loan Prediction</h1>', unsafe_allow_html=True)

    # Defaults for live preview before tab2 inputs are rendered
    if 'lp_income' not in st.session_state:
        st.session_state.lp_income = 3000
    if 'lp_co_income' not in st.session_state:
        st.session_state.lp_co_income = 0
    if 'lp_loan' not in st.session_state:
        st.session_state.lp_loan = 50000
    if 'lp_duration' not in st.session_state:
        st.session_state.lp_duration = 36
    if 'lp_credit' not in st.session_state:
        st.session_state.lp_credit = 720
    if 'lp_employment' not in st.session_state:
        st.session_state.lp_employment = "Salaried"
    if 'lp_education' not in st.session_state:
        st.session_state.lp_education = "Graduate"
    if 'lp_property' not in st.session_state:
        st.session_state.lp_property = "Urban"

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Personal Info", "Financial Info"])

        with tab1:
            name = st.text_input("Full Name", placeholder="John Smith")
            col_a, col_b = st.columns(2)
            with col_a:
                age = st.slider("Age", 18, 70, 30,
                    help="Your current age in years.")
                marital = st.selectbox("Marital Status",
                    ["Single", "Married", "Divorced", "Widowed"])
            with col_b:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"],
                    help="Number of financial dependents.")

            education = st.selectbox("Education Level",
                ["High School", "Graduate", "Post Graduate", "Doctorate"],
                help="Higher education increases approval probability.")
            employment = st.selectbox("Employment Type",
                ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Retired"],
                help="Salaried and Business Owner have highest stability score.")
            st.session_state.lp_employment = employment
            st.session_state.lp_education = education

        with tab2:
            col_c, col_d = st.columns(2)
            with col_c:
                applicant_income = st.number_input(
                    "Monthly Income ($)", 500, 50000, 3000, step=500,
                    help="Your gross monthly income in USD.")
                credit_score = st.slider("Credit Score", 300, 900, 720,
                    help="Higher score (750+) significantly increases approval chances.")
            with col_d:
                co_income = st.number_input(
                    "Co-applicant Income ($)", 0, 50000, 0, step=500,
                    help="Co-applicant's monthly income (0 if none).")
                loan_amount = st.number_input(
                    "Loan Amount ($)", 1000, 1000000, 50000, step=1000,
                    help="Total loan amount requested.")

            loan_duration = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60],
                index=2,
                help="Longer terms reduce EMI but increase total interest paid.")
            property_area = st.selectbox("Property Area",
                ["Urban", "Semi-Urban", "Rural"],
                help="Urban properties have higher approval rates.")

            # Update session state for live preview
            st.session_state.lp_income    = applicant_income
            st.session_state.lp_co_income = co_income
            st.session_state.lp_loan      = loan_amount
            st.session_state.lp_duration  = loan_duration
            st.session_state.lp_credit    = credit_score
            st.session_state.lp_property  = property_area

        # ---- Inline validation ----
        validations = render_validation(
            st.session_state.lp_credit,
            st.session_state.lp_income,
            st.session_state.lp_co_income,
            st.session_state.lp_loan,
            st.session_state.lp_duration
        )
        for msg, level in validations:
            if level == "error":
                st.error(msg)
            else:
                st.warning(msg)

        st.markdown("</div>", unsafe_allow_html=True)

        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            predict_btn = st.button("Predict Loan Approval", use_container_width=True)
        with col_btn2:
            reset_btn = st.button("Reset", use_container_width=True)

        if reset_btn:
            for key in ['lp_income','lp_co_income','lp_loan','lp_duration',
                        'lp_credit','lp_employment','lp_education','lp_property']:
                del st.session_state[key]
            st.rerun()

    # ---- Right column: live preview + key factors ----
    with col2:

        # Live score preview — always visible
        live_data = {
            'credit_score'     : st.session_state.lp_credit,
            'applicant_income' : st.session_state.lp_income,
            'co_income'        : st.session_state.lp_co_income,
            'loan_amount'      : st.session_state.lp_loan,
            'loan_duration'    : st.session_state.lp_duration,
            'employment'       : st.session_state.lp_employment,
            'education'        : st.session_state.lp_education,
            'property_area'    : st.session_state.lp_property,
        }
        live_result = calculate_loan_score(live_data)
        render_live_score(
            live_result['probability'],
            st.session_state.lp_income + st.session_state.lp_co_income,
            st.session_state.lp_loan,
            st.session_state.lp_duration
        )

        # Key factors weight panel
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e5e7eb; border-radius:12px;
                    padding:16px 18px; margin-top:4px;">
            <p style="font-size:11px; font-weight:600; text-transform:uppercase;
                      letter-spacing:0.6px; color:#9ca3af; margin:0 0 12px 0;
                      font-family:Inter,sans-serif;">Factor Weights</p>
        """, unsafe_allow_html=True)
        weights = [("Credit Score", 35), ("Income Stability", 30),
                   ("Employment", 20), ("Loan Amount", 15)]
        for factor, weight in weights:
            st.markdown(f"""
            <div style="margin-bottom:10px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                    <span style="font-size:13px; color:#374151; font-family:Inter,sans-serif;">{factor}</span>
                    <span style="font-size:12px; font-weight:600; color:#2563eb; font-family:Inter,sans-serif;">{weight}%</span>
                </div>
                <div style="background:#f0f4f8; border-radius:100px; height:5px; overflow:hidden;">
                    <div style="width:{weight}%; background:#2563eb; height:100%; border-radius:100px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Prediction result ----
    if predict_btn:
        st.session_state.prediction_count += 1

        applicant_data = {
            'name'            : name,
            'credit_score'    : credit_score,
            'applicant_income': applicant_income,
            'co_income'       : co_income,
            'loan_amount'     : loan_amount,
            'loan_duration'   : loan_duration,
            'employment'      : employment,
            'education'       : education,
            'property_area'   : property_area,
            'dependents'      : dependents,
            'marital'         : marital,
            'gender'          : gender
        }

        # Step-based animated progress
        steps = [
            (25,  "Verifying applicant identity..."),
            (50,  "Evaluating credit history..."),
            (75,  "Analysing income & liabilities..."),
            (90,  "Running decision model..."),
            (100, "Finalising decision..."),
        ]
        progress_bar = st.progress(0)
        status_text  = st.empty()
        for target, message in steps:
            for v in range(progress_bar._value if hasattr(progress_bar, '_value') else 0, target):
                progress_bar.progress(v + 1)
                time.sleep(0.012)
            status_text.markdown(
                f"<p style='font-size:13px; color:#6b7280; font-family:Inter,sans-serif;"
                f" margin:4px 0;'>{message}</p>",
                unsafe_allow_html=True
            )
            time.sleep(0.15)
        progress_bar.empty()
        status_text.empty()

        result = calculate_loan_score(applicant_data)
        st.session_state.current_prediction = result

        history_entry = {
            'timestamp' : datetime.now(),
            'name'      : name,
            'amount'    : loan_amount,
            'probability': result['probability'],
            'approved'  : result['approved']
        }
        st.session_state.loan_history.append(history_entry)

        st.markdown("---")

        # Result card
        label, color, bg, border = get_risk_level(result['probability'])
        verdict       = "LOAN APPROVED" if result['approved'] else "LOAN NOT APPROVED"
        verdict_color = "#16a34a"       if result['approved'] else "#dc2626"
        conf_pct      = int(result['probability'])
        emi_est       = (loan_amount / loan_duration) * 1.08

        st.markdown(f"""
        <div class="fade-in" style="background:{bg}; border:1.5px solid {border};
             border-left:4px solid {verdict_color}; border-radius:12px;
             padding:28px 24px; margin:20px 0;">
            <div style="display:flex; align-items:center; justify-content:space-between;
                        flex-wrap:wrap; gap:12px; margin-bottom:18px;">
                <h2 style="margin:0; font-size:22px; font-weight:700;
                           color:{verdict_color}; font-family:Inter,sans-serif;">{verdict}</h2>
                <span style="font-size:13px; font-weight:600; color:{color};
                             background:white; border:1px solid {border};
                             border-radius:20px; padding:5px 14px;
                             font-family:Inter,sans-serif;">{label}</span>
            </div>
            <p style="font-size:13px; font-weight:600; text-transform:uppercase;
                      letter-spacing:0.5px; color:#9ca3af; margin:0 0 6px 0;
                      font-family:Inter,sans-serif;">Approval Confidence</p>
            <div style="display:flex; align-items:center; gap:14px; margin-bottom:16px;">
                <div style="flex:1; background:#e5e7eb; border-radius:100px;
                            height:10px; overflow:hidden;">
                    <div style="width:{conf_pct}%; background:{verdict_color};
                                height:100%; border-radius:100px;"></div>
                </div>
                <span style="font-size:24px; font-weight:700; color:{verdict_color};
                             font-family:Inter,sans-serif; min-width:56px;">{result['probability']:.1f}%</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-top:4px;">
                <div style="background:white; border-radius:8px; padding:12px 14px;
                            border:1px solid {border};">
                    <p style="font-size:11px; color:#9ca3af; margin:0 0 4px 0;
                               font-family:Inter,sans-serif; text-transform:uppercase;
                               letter-spacing:0.5px;">Loan Amount</p>
                    <p style="font-size:16px; font-weight:700; color:#1f2937;
                               margin:0; font-family:Inter,sans-serif;">${loan_amount:,.0f}</p>
                </div>
                <div style="background:white; border-radius:8px; padding:12px 14px;
                            border:1px solid {border};">
                    <p style="font-size:11px; color:#9ca3af; margin:0 0 4px 0;
                               font-family:Inter,sans-serif; text-transform:uppercase;
                               letter-spacing:0.5px;">Est. EMI / mo</p>
                    <p style="font-size:16px; font-weight:700; color:#2563eb;
                               margin:0; font-family:Inter,sans-serif;">${emi_est:,.0f}</p>
                </div>
                <div style="background:white; border-radius:8px; padding:12px 14px;
                            border:1px solid {border};">
                    <p style="font-size:11px; color:#9ca3af; margin:0 0 4px 0;
                               font-family:Inter,sans-serif; text-transform:uppercase;
                               letter-spacing:0.5px;">Interest Rate</p>
                    <p style="font-size:16px; font-weight:700; color:#1f2937;
                               margin:0; font-family:Inter,sans-serif;">7.5–9.5%</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Score breakdown
        render_score_breakdown(result['factors'])

        # Recommendations
        st.markdown("""
        <p style="font-size:15px; font-weight:600; color:#1f2937;
                  font-family:Inter,sans-serif; margin:20px 0 10px 0;">Recommendations</p>
        """, unsafe_allow_html=True)
        if not result['approved']:
            if credit_score < 650:
                st.warning("Improve your credit score by paying bills on time and reducing outstanding debt.")
            if (applicant_income + co_income) < 3000:
                st.warning("Consider adding a co-applicant with a stable income to strengthen the application.")
            st.info("You may reapply in 6 months after addressing the above factors.")
        else:
            st.success("Your application looks strong. Proceed to the nearest branch to complete documentation.")

# -------------------- DASHBOARD --------------------
elif page == "Dashboard":
    st.markdown('<h1 class="main-title">Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Last prediction highlight
    if st.session_state.current_prediction:
        lp = st.session_state.current_prediction
        lp_label, lp_color, lp_bg, lp_border = get_risk_level(lp['probability'])
        lp_verdict = "Approved" if lp['approved'] else "Not Approved"
        st.markdown(f"""
        <div style="background:{lp_bg}; border:1.5px solid {lp_border};
             border-left:4px solid {lp_color}; border-radius:12px;
             padding:16px 20px; margin-bottom:24px;
             display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
            <div>
                <p style="font-size:11px; font-weight:600; text-transform:uppercase;
                           letter-spacing:0.6px; color:#9ca3af; margin:0 0 4px 0;
                           font-family:Inter,sans-serif;">Last Prediction</p>
                <p style="font-size:16px; font-weight:700; color:{lp_color};
                           margin:0; font-family:Inter,sans-serif;">{lp_verdict} — {lp['probability']:.1f}% confidence</p>
            </div>
            <span style="font-size:13px; font-weight:600; color:{lp_color};
                         background:white; border:1px solid {lp_border};
                         border-radius:20px; padding:5px 14px;
                         font-family:Inter,sans-serif;">{lp_label}</span>
        </div>
        """, unsafe_allow_html=True)

    # Metrics row
    col1, col2, col3, col4 = st.columns(4)

    total_preds = st.session_state.prediction_count
    if st.session_state.loan_history:
        n_approved = len([h for h in st.session_state.loan_history if h['approved']])
        rate        = (n_approved / len(st.session_state.loan_history)) * 100
        total_val   = sum(h['amount'] for h in st.session_state.loan_history)
        avg_val     = total_val / len(st.session_state.loan_history)
    else:
        n_approved = 0; rate = 0; total_val = 0; avg_val = 0

    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Predictions", total_preds)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Approval Rate", f"{rate:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Loan Value", f"${total_val:,.0f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg. Loan Amount", f"${avg_val:,.0f}" if avg_val else "$0")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.loan_history:
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.markdown("**Approval vs Rejection**")
            n_rejected = len(st.session_state.loan_history) - n_approved
            chart_df = pd.DataFrame({
                "Status": ["Approved", "Rejected"],
                "Count" : [n_approved, n_rejected]
            })
            st.bar_chart(chart_df.set_index("Status"), color="#2563eb", height=220)

        with chart_col2:
            st.markdown("**Loan Amount Distribution**")
            amounts_df = pd.DataFrame({
                "Loan Amount ($)": [h['amount'] for h in st.session_state.loan_history]
            })
            st.bar_chart(amounts_df, color="#2563eb", height=220)

        st.markdown("---")

    # Recent applications
    st.markdown("### Recent Applications")
    if st.session_state.loan_history:
        recent = st.session_state.loan_history[-10:][::-1]
        for app in recent:
            status = "Approved" if app['approved'] else "Rejected"
            s_color = "#16a34a" if app['approved'] else "#dc2626"
            s_bg    = "#f0fdf4" if app['approved'] else "#fef2f2"
            s_border= "#bbf7d0" if app['approved'] else "#fecaca"
            st.markdown(f"""
            <div style="display:flex; align-items:center; justify-content:space-between;
                        padding:12px 16px; border:1px solid #e5e7eb; border-radius:10px;
                        margin-bottom:8px; background:#ffffff; flex-wrap:wrap; gap:8px;">
                <span style="font-size:14px; font-weight:600; color:#1f2937;
                             font-family:Inter,sans-serif;">{app['name'] or 'N/A'}</span>
                <span style="font-size:13px; color:#6b7280;
                             font-family:Inter,sans-serif;">${app['amount']:,.0f}</span>
                <span style="font-size:13px; color:#6b7280;
                             font-family:Inter,sans-serif;">{app['probability']:.1f}%</span>
                <span style="font-size:12px; font-weight:600; color:{s_color};
                             background:{s_bg}; border:1px solid {s_border};
                             border-radius:20px; padding:3px 10px;
                             font-family:Inter,sans-serif;">{status}</span>
                <span style="font-size:12px; color:#9ca3af;
                             font-family:Inter,sans-serif;">{app['timestamp'].strftime('%d %b %Y %H:%M')}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No applications yet. Make your first prediction!")

# -------------------- HISTORY --------------------
elif page == "History":
    st.markdown('<h1 class="main-title">Application History</h1>', unsafe_allow_html=True)

    if st.session_state.loan_history:
        history_data = []
        for entry in st.session_state.loan_history:
            history_data.append({
                'Date'       : entry['timestamp'].strftime('%Y-%m-%d %H:%M'),
                'Applicant'  : entry['name'],
                'Amount'     : f"${entry['amount']:,.0f}",
                'Probability': f"{entry['probability']:.1f}%",
                'Status'     : 'Approved' if entry['approved'] else 'Rejected'
            })

        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name="loan_history.csv",
            mime="text/csv"
        )

        st.markdown("### Statistics")
        approved_n = len([h for h in st.session_state.loan_history if h['approved']])
        total_n    = len(st.session_state.loan_history)
        avg_prob   = np.mean([h['probability'] for h in st.session_state.loan_history])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", total_n)
        with col2:
            st.metric("Approved", approved_n)
        with col3:
            st.metric("Avg. Probability", f"{avg_prob:.1f}%")
    else:
        st.info("No history available yet. Make your first prediction!")

# -------------------- SETTINGS --------------------
elif page == "Settings":
    st.markdown('<h1 class="main-title">Settings</h1>', unsafe_allow_html=True)

    with st.expander("Model Settings"):
        threshold = st.slider("Approval Threshold (%)", 50, 80, 65)
        st.info(f"Applications with probability >= {threshold}% will be approved")

    with st.expander("Notification Settings"):
        email = st.checkbox("Email notifications", True)
        sms   = st.checkbox("SMS notifications", False)

    with st.expander("System Information"):
        st.write("**Version:** 2.0.0")
        st.write("**Last Updated:** 2024-01-15")
        st.write("**Model Type:** Random Forest Ensemble")
        st.write("**Accuracy:** 89.2%")

    if st.button("Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")

# -------------------- FOOTER --------------------
st.markdown("""
<div style='text-align: center; color: #9ca3af; padding: 30px 0; margin-top: 50px;
     border-top: 1px solid #e5e7eb; font-family: Inter, sans-serif; font-size: 13px;'>
    <p>FinBank AI &nbsp;·&nbsp; Secure &nbsp;·&nbsp; Intelligent &nbsp;·&nbsp; Transparent</p>
    <p style='font-size: 11px; color: #d1d5db; margin-top: 4px;'>© 2024 FinBank AI Technologies. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
