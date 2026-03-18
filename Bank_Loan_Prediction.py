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

# -------------------- PREMIUM CSS --------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/*
  COLOR PALETTE
  --dark-green  : #25671E  (deep forest — backgrounds, sidebar, dark surfaces)
  --bright-green: #48A111  (vivid lime — primary accent, buttons, highlights)
  --gold        : #F2B50B  (warm amber — secondary accent, titles, stars)
  --cream       : #F7F0F0  (soft white — text, light surfaces)
*/

:root {
    --dark-green  : #25671E;
    --bright-green: #48A111;
    --gold        : #F2B50B;
    --cream       : #F7F0F0;
    --bg-base     : #0f1f0d;
    --bg-surface  : rgba(37, 103, 30, 0.35);
    --bg-glass    : rgba(15, 31, 13, 0.75);
    --border-dim  : rgba(72, 161, 17, 0.18);
    --border-gold : rgba(242, 181, 11, 0.25);
    --text-muted  : rgba(247, 240, 240, 0.5);
    --text-dim    : rgba(247, 240, 240, 0.35);
}

/* ============================================================
   GLOBAL RESET & BASE
   ============================================================ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    font-family: 'DM Sans', sans-serif !important;
    background: var(--bg-base) !important;
    color: var(--cream) !important;
}

/* Animated mesh background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 15% 20%, rgba(37,103,30,0.45) 0%, transparent 60%),
        radial-gradient(ellipse 60% 45% at 85% 80%, rgba(72,161,17,0.20) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 55% 5%,  rgba(242,181,11,0.06) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
    animation: meshShift 14s ease-in-out infinite alternate;
}

@keyframes meshShift {
    0%   { opacity: 1;    transform: scale(1)    translateY(0px); }
    100% { opacity: 0.82; transform: scale(1.04) translateY(-12px); }
}

/* Particle dot grid overlay */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(circle, rgba(72,161,17,0.07) 1px, transparent 1px),
        radial-gradient(circle, rgba(242,181,11,0.04) 1px, transparent 1px);
    background-size: 58px 58px, 86px 86px;
    background-position: 0 0, 29px 29px;
    pointer-events: none;
    z-index: 0;
    animation: particleDrift 22s linear infinite;
}

@keyframes particleDrift {
    from { background-position: 0 0, 29px 29px; }
    to   { background-position: 58px 58px, 86px 86px; }
}

[data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 1;
}

/* ============================================================
   MAIN TITLE
   ============================================================ */
.main-title {
    font-family: 'Syne', sans-serif !important;
    background: linear-gradient(110deg,
        var(--gold) 0%,
        var(--cream) 35%,
        var(--bright-green) 65%,
        var(--gold) 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: clamp(32px, 5vw, 54px);
    font-weight: 800;
    text-align: center;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 6px;
    animation: titleShimmer 4s linear infinite, slideDown 0.7s cubic-bezier(0.16,1,0.3,1) both;
}

@keyframes titleShimmer {
    0%   { background-position: 0%   center; }
    100% { background-position: 200% center; }
}

@keyframes slideDown {
    from { opacity: 0; transform: translateY(-24px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ============================================================
   SIDEBAR — DARK GLASS
   ============================================================ */
[data-testid="stSidebar"] {
    background: rgba(10, 22, 8, 0.92) !important;
    backdrop-filter: blur(28px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(28px) saturate(160%) !important;
    border-right: 1px solid var(--border-dim) !important;
    box-shadow: 4px 0 40px rgba(0,0,0,0.55) !important;
}

[data-testid="stSidebar"] * {
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] h2 {
    font-family: 'Syne', sans-serif !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, var(--gold), var(--bright-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: block;
    padding: 10px 16px !important;
    border-radius: 10px !important;
    margin: 3px 0 !important;
    transition: all 0.25s ease !important;
    cursor: pointer !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    border: 1px solid transparent !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(72,161,17,0.12) !important;
    border-color: rgba(72,161,17,0.25) !important;
    transform: translateX(4px) !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(72,161,17,0.07) !important;
    border: 1px solid rgba(72,161,17,0.15) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 6px 0 !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"]:hover {
    background: rgba(72,161,17,0.14) !important;
    border-color: rgba(72,161,17,0.3) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--text-muted) !important;
}

[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 24px !important;
    font-weight: 700 !important;
    color: var(--gold) !important;
}

/* ============================================================
   BUTTONS — GOLD → GREEN GRADIENT
   ============================================================ */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    padding: 14px 28px !important;
    border-radius: 14px !important;
    border: none !important;
    background: linear-gradient(135deg,
        var(--dark-green) 0%,
        var(--bright-green) 45%,
        #6abf1a 75%,
        var(--gold) 100%) !important;
    background-size: 200% 200% !important;
    color: var(--cream) !important;
    position: relative !important;
    overflow: hidden !important;
    transition: all 0.3s cubic-bezier(0.16,1,0.3,1) !important;
    box-shadow:
        0 4px 18px rgba(72,161,17,0.4),
        0 1px 4px rgba(0,0,0,0.4),
        inset 0 1px 0 rgba(247,240,240,0.12) !important;
    animation: gradientShift 4s ease infinite !important;
}

@keyframes gradientShift {
    0%, 100% { background-position: 0%   50%; }
    50%       { background-position: 100% 50%; }
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(247,240,240,0.18), transparent);
    transition: left 0.5s ease;
    transform: skewX(-20deg);
}

.stButton > button:hover {
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow:
        0 8px 28px rgba(72,161,17,0.55),
        0 4px 12px rgba(242,181,11,0.25),
        inset 0 1px 0 rgba(247,240,240,0.18) !important;
}

.stButton > button:hover::before { left: 150%; }

.stButton > button:active {
    transform: translateY(1px) scale(0.98) !important;
    box-shadow: 0 2px 8px rgba(72,161,17,0.3) !important;
}

/* ============================================================
   INPUT FIELDS
   ============================================================ */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(37,103,30,0.12) !important;
    border: 1px solid rgba(72,161,17,0.2) !important;
    border-radius: 12px !important;
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 12px 16px !important;
    transition: all 0.3s ease !important;
    box-shadow: inset 0 2px 6px rgba(0,0,0,0.25) !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(72,161,17,0.55) !important;
    box-shadow:
        inset 0 2px 6px rgba(0,0,0,0.2),
        0 0 0 3px rgba(72,161,17,0.13),
        0 0 20px rgba(242,181,11,0.06) !important;
    background: rgba(37,103,30,0.18) !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stNumberInput"] input::placeholder {
    color: rgba(247,240,240,0.3) !important;
    font-style: italic !important;
}

/* ============================================================
   SELECT BOXES
   ============================================================ */
[data-testid="stSelectbox"] > div > div {
    background: rgba(37,103,30,0.12) !important;
    border: 1px solid rgba(72,161,17,0.2) !important;
    border-radius: 12px !important;
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.3s ease !important;
}

[data-testid="stSelectbox"] > div > div:hover {
    border-color: rgba(72,161,17,0.45) !important;
    box-shadow: 0 0 0 3px rgba(72,161,17,0.09) !important;
}

/* ============================================================
   SLIDER
   ============================================================ */
[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
    background: linear-gradient(135deg, var(--dark-green), var(--gold)) !important;
    box-shadow: 0 0 12px rgba(242,181,11,0.5) !important;
}

[data-testid="stSlider"] div[data-baseweb="slider"] div:first-child {
    background: linear-gradient(90deg, var(--bright-green), var(--gold)) !important;
}

/* ============================================================
   TABS — PILL STYLE
   ============================================================ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(37,103,30,0.15) !important;
    border: 1px solid rgba(72,161,17,0.15) !important;
    border-radius: 16px !important;
    padding: 4px !important;
    gap: 4px !important;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    color: rgba(247,240,240,0.55) !important;
    border-radius: 12px !important;
    padding: 8px 20px !important;
    transition: all 0.25s ease !important;
    border: none !important;
    background: transparent !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: var(--cream) !important;
    background: rgba(72,161,17,0.12) !important;
}

[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(37,103,30,0.65), rgba(72,161,17,0.45)) !important;
    color: var(--cream) !important;
    box-shadow: 0 2px 12px rgba(72,161,17,0.3), 0 0 0 1px rgba(242,181,11,0.15) !important;
}

[data-baseweb="tab-highlight"] { display: none !important; }
[data-baseweb="tab-border"]    { display: none !important; }

/* ============================================================
   PROGRESS BARS — ANIMATED GRADIENT
   ============================================================ */
[data-testid="stProgress"] > div > div > div > div {
    background: linear-gradient(90deg,
        var(--dark-green),
        var(--bright-green),
        var(--gold),
        var(--bright-green),
        var(--dark-green)) !important;
    background-size: 200% 100% !important;
    border-radius: 100px !important;
    animation: progressFlow 2.5s linear infinite !important;
    box-shadow: 0 0 10px rgba(72,161,17,0.45) !important;
}

@keyframes progressFlow {
    0%   { background-position: 0%   0%; }
    100% { background-position: 200% 0%; }
}

[data-testid="stProgress"] > div > div > div {
    background: rgba(37,103,30,0.18) !important;
    border-radius: 100px !important;
    height: 8px !important;
    overflow: hidden !important;
}

/* ============================================================
   CARDS — GLASS MORPHISM
   ============================================================ */
.form-card {
    background: rgba(10, 25, 8, 0.72) !important;
    backdrop-filter: blur(20px) saturate(160%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
    border: 1px solid rgba(72,161,17,0.14) !important;
    border-radius: 24px !important;
    padding: 32px !important;
    margin-bottom: 24px !important;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(247,240,240,0.04),
        inset 0 -1px 0 rgba(0,0,0,0.2) !important;
    transition: all 0.35s cubic-bezier(0.16,1,0.3,1) !important;
    animation: fadeSlideUp 0.6s cubic-bezier(0.16,1,0.3,1) both !important;
}

.form-card:hover {
    border-color: rgba(72,161,17,0.28) !important;
    box-shadow:
        0 16px 48px rgba(0,0,0,0.5),
        0 0 0 1px rgba(242,181,11,0.07),
        inset 0 1px 0 rgba(247,240,240,0.06) !important;
    transform: translateY(-2px) !important;
}

.metric-card {
    background: rgba(10, 25, 8, 0.72) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(72,161,17,0.14) !important;
    border-radius: 20px !important;
    padding: 24px 20px !important;
    text-align: center !important;
    margin: 8px 0 !important;
    transition: all 0.35s cubic-bezier(0.16,1,0.3,1) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35) !important;
    animation: fadeSlideUp 0.5s cubic-bezier(0.16,1,0.3,1) both !important;
}

.metric-card:hover {
    border-color: rgba(242,181,11,0.25) !important;
    transform: translateY(-4px) !important;
    box-shadow:
        0 12px 40px rgba(0,0,0,0.5),
        0 0 30px rgba(72,161,17,0.07) !important;
}

/* ============================================================
   RESULT CARDS
   ============================================================ */
.approved-card {
    background: rgba(8, 28, 6, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(72,161,17,0.4) !important;
    border-left: 5px solid var(--bright-green) !important;
    border-radius: 20px !important;
    padding: 32px 28px !important;
    margin: 24px 0 !important;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.45),
        0 0 60px rgba(72,161,17,0.09),
        inset 0 1px 0 rgba(72,161,17,0.1) !important;
    animation: approvedPulse 2.5s ease-in-out infinite, fadeSlideUp 0.6s cubic-bezier(0.16,1,0.3,1) both !important;
    position: relative !important;
    overflow: hidden !important;
}

.approved-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0%, rgba(72,161,17,0.05) 25%, transparent 50%);
    animation: rotateSlow 8s linear infinite;
}

@keyframes approvedPulse {
    0%, 100% { box-shadow: 0 8px 32px rgba(0,0,0,0.45), 0 0 30px rgba(72,161,17,0.07); }
    50%       { box-shadow: 0 8px 32px rgba(0,0,0,0.45), 0 0 70px rgba(72,161,17,0.18), 0 0 120px rgba(242,181,11,0.05); }
}

@keyframes rotateSlow {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}

.rejected-card {
    background: rgba(30, 8, 8, 0.72) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(220,53,69,0.28) !important;
    border-left: 5px solid #dc3545 !important;
    border-radius: 20px !important;
    padding: 32px 28px !important;
    margin: 24px 0 !important;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.45),
        0 0 40px rgba(220,53,69,0.07),
        inset 0 1px 0 rgba(220,53,69,0.07) !important;
    animation: fadeSlideUp 0.6s cubic-bezier(0.16,1,0.3,1) both !important;
}

/* ============================================================
   TYPOGRAPHY
   ============================================================ */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.5px !important;
    color: var(--cream) !important;
}

h3 {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: rgba(247,240,240,0.88) !important;
    letter-spacing: 0px !important;
}

p, label, span, div {
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stWidgetLabel"] p,
label {
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    color: rgba(247,240,240,0.48) !important;
    margin-bottom: 6px !important;
}

/* ============================================================
   METRICS (MAIN AREA)
   ============================================================ */
[data-testid="stMetric"] {
    background: rgba(10, 25, 8, 0.68) !important;
    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(72,161,17,0.14) !important;
    border-radius: 18px !important;
    padding: 20px !important;
    transition: all 0.3s ease !important;
    animation: fadeSlideUp 0.5s ease both !important;
}

[data-testid="stMetric"]:hover {
    border-color: rgba(242,181,11,0.25) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.45), 0 0 20px rgba(72,161,17,0.07) !important;
}

[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: rgba(200, 216, 234, 0.5) !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
    color: var(--cream) !important;
    background: linear-gradient(135deg, var(--gold), var(--bright-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ============================================================
   INFO / WARNING / SUCCESS BOXES
   ============================================================ */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(72,161,17,0.15) !important;
    animation: fadeSlideUp 0.4s ease both !important;
}

[data-testid="stAlert"][data-baseweb="notification"][kind="info"] {
    background: rgba(37,103,30,0.18) !important;
    border-color: rgba(72,161,17,0.3) !important;
}

[data-testid="stAlert"][kind="warning"] {
    background: rgba(242,181,11,0.1) !important;
    border-color: rgba(242,181,11,0.28) !important;
}

[data-testid="stAlert"][kind="success"] {
    background: rgba(72,161,17,0.13) !important;
    border-color: rgba(72,161,17,0.32) !important;
}

/* ============================================================
   DATAFRAME
   ============================================================ */
[data-testid="stDataFrame"] {
    border-radius: 18px !important;
    overflow: hidden !important;
    border: 1px solid rgba(72,161,17,0.14) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35) !important;
}

/* ============================================================
   EXPANDERS
   ============================================================ */
[data-testid="stExpander"] {
    background: rgba(10, 25, 8, 0.65) !important;
    border: 1px solid rgba(72,161,17,0.14) !important;
    border-radius: 16px !important;
    margin-bottom: 10px !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.3s ease !important;
}

[data-testid="stExpander"]:hover {
    border-color: rgba(242,181,11,0.22) !important;
}

[data-testid="stExpander"] summary {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    color: var(--cream) !important;
    padding: 14px 16px !important;
}

/* ============================================================
   DIVIDERS
   ============================================================ */
hr {
    border: none !important;
    border-top: 1px solid rgba(72,161,17,0.12) !important;
    margin: 24px 0 !important;
}

/* ============================================================
   SCROLLBAR
   ============================================================ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: rgba(37,103,30,0.08); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--dark-green), var(--gold));
    border-radius: 100px;
}

/* ============================================================
   STICKY HEADER EFFECT
   ============================================================ */
header[data-testid="stHeader"] {
    background: rgba(8, 18, 6, 0.92) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-bottom: 1px solid rgba(72,161,17,0.12) !important;
}

/* ============================================================
   SHIMMER LOADING
   ============================================================ */
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position:  200% 0; }
}

.shimmer {
    background: linear-gradient(90deg,
        rgba(37,103,30,0.06) 25%,
        rgba(72,161,17,0.12) 50%,
        rgba(37,103,30,0.06) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 10px;
}

/* ============================================================
   KEYFRAME UTILITIES
   ============================================================ */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

.fade-in {
    animation: fadeSlideUp 0.6s cubic-bezier(0.16,1,0.3,1) both !important;
}

/* ============================================================
   TOOLTIP EFFECT
   ============================================================ */
[data-testid="stWidgetLabel"] p::after {
    content: attr(data-tooltip);
    position: absolute;
    background: rgba(8, 18, 6, 0.96);
    color: var(--cream);
    padding: 5px 10px;
    border-radius: 8px;
    font-size: 11px;
    white-space: nowrap;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s ease;
    border: 1px solid rgba(72,161,17,0.25);
    z-index: 999;
}

/* ============================================================
   DOWNLOAD BUTTON
   ============================================================ */
[data-testid="stDownloadButton"] > button {
    background: rgba(37,103,30,0.2) !important;
    border: 1px solid rgba(72,161,17,0.35) !important;
    color: var(--gold) !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background: rgba(72,161,17,0.2) !important;
    border-color: rgba(242,181,11,0.45) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(72,161,17,0.28) !important;
}

/* ============================================================
   CAPTION / SMALL TEXT
   ============================================================ */
[data-testid="stCaptionContainer"] p {
    color: rgba(247,240,240,0.38) !important;
    font-size: 12px !important;
    letter-spacing: 0.3px !important;
}

/* ============================================================
   SUCCESS CONFETTI GLOW
   ============================================================ */
@keyframes confettiGlow {
    0%   { box-shadow: 0 0 20px rgba(72,161,17,0.2); }
    25%  { box-shadow: 0 0 40px rgba(72,161,17,0.4), 0 0 80px rgba(242,181,11,0.08); }
    50%  { box-shadow: 0 0 60px rgba(72,161,17,0.5), 0 0 120px rgba(242,181,11,0.1); }
    75%  { box-shadow: 0 0 40px rgba(72,161,17,0.3); }
    100% { box-shadow: 0 0 20px rgba(72,161,17,0.18); }
}

/* ============================================================
   FOOTER
   ============================================================ */
footer, [data-testid="stFooter"] {
    background: transparent !important;
}

</style>

<!-- Floating particles canvas injected via HTML -->
<canvas id="particleCanvas" style="
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 0;
    opacity: 0.35;
"></canvas>

<script>
(function() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = Array.from({length: 38}, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.5 + 0.3,
        dx: (Math.random() - 0.5) * 0.3,
        dy: (Math.random() - 0.5) * 0.3,
        alpha: Math.random() * 0.5 + 0.15,
        color: Math.random() > 0.5 ? '72,161,17' : '242,181,11'
    }));

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => {
            p.x += p.dx; p.y += p.dy;
            if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
            if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${p.color},${p.alpha})`;
            ctx.fill();
        });

        // Draw connecting lines between nearby particles
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(72,161,17,${0.07 * (1 - dist/120)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
})();
</script>
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
<div style='text-align: center; color: rgba(247,240,240,0.28); padding: 30px 0; margin-top: 50px; border-top: 1px solid rgba(72,161,17,0.1); font-family: DM Sans, sans-serif; font-size: 13px; letter-spacing: 0.3px;'>
    <p>🏦 FinBank AI &nbsp;·&nbsp; Secure &nbsp;·&nbsp; Intelligent &nbsp;·&nbsp; Transparent</p>
    <p style='font-size: 11px; color: rgba(247,240,240,0.15); margin-top: 6px;'>© 2024 FinBank AI Technologies. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
