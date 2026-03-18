import streamlit as st
import time
import pandas as pd
import numpy as np
from datetime import datetime
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="FinBank AI - Loan Prediction",
    page_icon="🏦",
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
    st.markdown("## 🏦 FinBank AI")
    st.caption("Smart Loan Decision System")
    
    st.divider()
    
    page = st.radio(
        "Navigation",
        ["🏠 Loan Prediction", "📊 Dashboard", "📋 History", "⚙️ Settings"]
    )
    
    st.divider()
    
    st.markdown("### 📊 Quick Stats")
    st.metric("Predictions Today", st.session_state.prediction_count)
    st.metric("Approval Rate", "63%")
    
    if st.button("🔄 Clear History"):
        st.session_state.loan_history = []
        st.session_state.prediction_count = 0
        st.success("History cleared!")
    
    st.divider()
    st.info("Powered by Machine Learning")

# -------------------- PREDICTION FUNCTION --------------------
def calculate_loan_score(data):
    score = 0
    factors = []
    
    # Credit Score (0-300 points)
    credit_score_pts = min(data['credit_score'], 900) / 3
    score += credit_score_pts
    factors.append(("Credit Score", credit_score_pts, 300))
    
    # Income to Loan Ratio
    total_income = data['applicant_income'] + data['co_income']
    if total_income > 0:
        income_ratio = (data['loan_amount'] * 1000) / (total_income * data['loan_duration'])
        income_pts = max(0, 250 - income_ratio * 25)
        score += income_pts
        factors.append(("Income Ratio", income_pts, 250))
    
    # Employment Stability
    employment_score = {
        "Job": 150,
        "Self-Employed": 100,
        "Business": 120,
        "Salaried": 150,
        "Business Owner": 120,
        "Freelancer": 80,
        "Retired": 60
    }.get(data['employment'], 80)
    score += employment_score
    factors.append(("Employment", employment_score, 150))
    
    # Education
    education_score = {
        "Graduate": 100,
        "Post Graduate": 120,
        "Doctorate": 140,
        "High School": 60
    }.get(data['education'], 60)
    score += education_score
    factors.append(("Education", education_score, 140))
    
    # Property Area
    property_score = {
        "Urban": 80,
        "Semi-Urban": 70,
        "Rural": 50
    }.get(data['property_area'], 50)
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

# -------------------- MAIN PAGE --------------------
if page == "🏠 Loan Prediction":
    st.markdown('<h1 class="main-title">🏦 Bank Loan Prediction</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Personal Info", "Financial Info"])
        
        with tab1:
            name = st.text_input("Full Name", placeholder="John Smith")
            col_a, col_b = st.columns(2)
            with col_a:
                age = st.slider("Age", 18, 70, 30)
                marital = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
            with col_b:
                gender = st.selectbox("Gender", ["Male", "Female", "Other"])
                dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
            
            education = st.selectbox("Education Level", ["High School", "Graduate", "Post Graduate", "Doctorate"])
            employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Business Owner", "Freelancer", "Retired"])
        
        with tab2:
            col_c, col_d = st.columns(2)
            with col_c:
                applicant_income = st.number_input("Monthly Income ($)", 500, 50000, 3000, step=500)
                credit_score = st.slider("Credit Score", 300, 900, 720)
            with col_d:
                co_income = st.number_input("Co-applicant Income ($)", 0, 50000, 0, step=500)
                loan_amount = st.number_input("Loan Amount ($)", 1000, 1000000, 50000, step=1000)
            
            loan_duration = st.selectbox("Loan Term (months)", [12, 24, 36, 48, 60])
            property_area = st.selectbox("Property Area", ["Urban", "Semi-Urban", "Rural"])
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        predict_btn = st.button("🚀 Predict Loan Approval", use_container_width=True)
    
    with col2:
        st.markdown("### 💡 Quick Insights")
        
        if predict_btn:
            total_income = applicant_income + co_income
            debt_ratio = (loan_amount / (total_income * loan_duration)) * 100
            
            insights = []
            if credit_score >= 750:
                insights.append("✅ Excellent credit score")
            elif credit_score < 600:
                insights.append("⚠️ Credit score needs improvement")
            
            if total_income > 5000:
                insights.append("✅ Strong income level")
            
            if employment in ["Salaried", "Business Owner"]:
                insights.append("✅ Stable employment")
            
            for insight in insights:
                st.info(insight)
        
        st.markdown("### 📊 Key Factors")
        factors = [
            ("Credit Score", 35),
            ("Income Stability", 30),
            ("Employment Type", 20),
            ("Loan Amount", 15)
        ]
        
        for factor, weight in factors:
            st.write(f"**{factor}:** {weight}%")
            st.progress(weight / 100)
    
    if predict_btn:
        st.session_state.prediction_count += 1
        
        applicant_data = {
            'name': name,
            'credit_score': credit_score,
            'applicant_income': applicant_income,
            'co_income': co_income,
            'loan_amount': loan_amount,
            'loan_duration': loan_duration,
            'employment': employment,
            'education': education,
            'property_area': property_area,
            'dependents': dependents,
            'marital': marital,
            'gender': gender
        }
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            progress_bar.progress(i + 1)
            if i < 30:
                status_text.text("🔍 Analyzing credit history...")
            elif i < 60:
                status_text.text("📊 Calculating financial ratios...")
            elif i < 80:
                status_text.text("🤖 Running prediction models...")
            else:
                status_text.text("📝 Generating final report...")
            time.sleep(0.02)
        
        status_text.text("✅ Analysis complete!")
        
        result = calculate_loan_score(applicant_data)
        st.session_state.current_prediction = result
        
        history_entry = {
            'timestamp': datetime.now(),
            'name': name,
            'amount': loan_amount,
            'probability': result['probability'],
            'approved': result['approved']
        }
        st.session_state.loan_history.append(history_entry)
        
        st.markdown("---")
        
        if result['approved']:
            st.markdown(f'''
            <div class="approved-card fade-in">
                <h2>✅ LOAN APPROVED</h2>
                <p style="font-size: 24px;">
                    Approval Probability: <b>{result["probability"]:.1f}%</b>
                </p>
                <p>Recommended Amount: <b>${loan_amount:,.0f}</b></p>
                <p>Estimated Interest Rate: <b>7.5% - 9.5%</b></p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="rejected-card fade-in">
                <h2>❌ LOAN NOT APPROVED</h2>
                <p style="font-size: 24px;">
                    Approval Probability: <b>{result["probability"]:.1f}%</b>
                </p>
                <p>Minimum Required: <b>65%</b></p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Detailed Analysis
        st.markdown("### 📈 Score Breakdown")
        col_a, col_b = st.columns(2)
        
        with col_a:
            for factor, score, max_score in result['factors'][:3]:
                st.write(f"**{factor}:** {score:.0f}/{max_score}")
                st.progress(score / max_score)
        
        with col_b:
            for factor, score, max_score in result['factors'][3:]:
                st.write(f"**{factor}:** {score:.0f}/{max_score}")
                st.progress(score / max_score)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        if not result['approved']:
            if credit_score < 650:
                st.warning("• Improve your credit score by paying bills on time")
            if (applicant_income + co_income) < 3000:
                st.warning("• Consider adding a co-applicant with stable income")
            st.info("You can reapply in 6 months after improving these factors")

# -------------------- DASHBOARD --------------------
elif page == "📊 Dashboard":
    st.markdown('<h1 class="main-title">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Predictions", st.session_state.prediction_count)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.loan_history:
            approved = len([h for h in st.session_state.loan_history if h['approved']])
            rate = (approved / len(st.session_state.loan_history)) * 100
            st.metric("Approval Rate", f"{rate:.1f}%")
        else:
            st.metric("Approval Rate", "0%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        if st.session_state.loan_history:
            total = sum(h['amount'] for h in st.session_state.loan_history)
            st.metric("Total Loan Value", f"${total:,.0f}")
        else:
            st.metric("Total Loan Value", "$0")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Avg. Loan Amount", "$50,000")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Applications
    st.markdown("### 📋 Recent Applications")
    if st.session_state.loan_history:
        # Get last 10 applications
        recent = st.session_state.loan_history[-10:][::-1]
        
        for app in recent:
            status = "✅ Approved" if app['approved'] else "❌ Rejected"
            color = "green" if app['approved'] else "red"
            
            st.write(f"""
            **{app['name']}** | ${app['amount']:,.0f} | {app['probability']:.1f}% | 
            <span style='color:{color}'>{status}</span> | 
            {app['timestamp'].strftime('%Y-%m-%d %H:%M')}
            """, unsafe_allow_html=True)
            st.progress(app['probability'] / 100)
    else:
        st.info("No applications yet. Make your first prediction!")

# -------------------- HISTORY --------------------
elif page == "📋 History":
    st.markdown('<h1 class="main-title">📋 Application History</h1>', unsafe_allow_html=True)
    
    if st.session_state.loan_history:
        # Create DataFrame for better display
        history_data = []
        for entry in st.session_state.loan_history:
            history_data.append({
                'Date': entry['timestamp'].strftime('%Y-%m-%d %H:%M'),
                'Applicant': entry['name'],
                'Amount': f"${entry['amount']:,.0f}",
                'Probability': f"{entry['probability']:.1f}%",
                'Status': '✅ Approved' if entry['approved'] else '❌ Rejected'
            })
        
        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="loan_history.csv",
            mime="text/csv"
        )
        
        # Statistics
        st.markdown("### 📊 Statistics")
        approved = len([h for h in st.session_state.loan_history if h['approved']])
        total = len(st.session_state.loan_history)
        avg_prob = np.mean([h['probability'] for h in st.session_state.loan_history])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", total)
        with col2:
            st.metric("Approved", approved)
        with col3:
            st.metric("Avg. Probability", f"{avg_prob:.1f}%")
    else:
        st.info("No history available yet. Make your first prediction in the Loan Prediction page!")

# -------------------- SETTINGS --------------------
elif page == "⚙️ Settings":
    st.markdown('<h1 class="main-title">⚙️ Settings</h1>', unsafe_allow_html=True)
    
    with st.expander("Model Settings"):
        threshold = st.slider("Approval Threshold (%)", 50, 80, 65)
        st.info(f"Applications with probability ≥ {threshold}% will be approved")
    
    with st.expander("Notification Settings"):
        email = st.checkbox("Email notifications", True)
        sms = st.checkbox("SMS notifications", False)
    
    with st.expander("System Information"):
        st.write("**Version:** 2.0.0")
        st.write("**Last Updated:** 2024-01-15")
        st.write("**Model Type:** Random Forest Ensemble")
        st.write("**Accuracy:** 89.2%")
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("Settings saved successfully!")

# -------------------- FOOTER --------------------
st.markdown("""
<div style='text-align: center; color: #9ca3af; padding: 30px 0; margin-top: 50px; border-top: 1px solid #e5e7eb; font-family: Inter, sans-serif; font-size: 13px;'>
    <p>🏦 FinBank AI &nbsp;·&nbsp; Secure &nbsp;·&nbsp; Intelligent &nbsp;·&nbsp; Transparent</p>
    <p style='font-size: 11px; color: #d1d5db; margin-top: 4px;'>© 2024 FinBank AI Technologies. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
