"""Application visual theme.

Original healthcare/data-analytics design.
Designed for the COVID-19 Pandemic Trend Analysis dashboard.
"""

from __future__ import annotations


APP_CSS = """
<style>

/* =========================================================
   GLOBAL THEME
   ========================================================= */

@import url("https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&display=swap");

html,
body,
[class*="css"] {
    font-family: "Source Sans 3", "Segoe UI", Helvetica, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(15, 76, 92, 0.035),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(13, 148, 136, 0.025),
            transparent 28%
        ),
        #f4f7f9;

    color: #0b1f33 !important;
}

/* Main content */

.block-container {
    max-width: 1280px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Remove excessive Streamlit spacing */

[data-testid="stVerticalBlock"] {
    gap: 0.7rem;
}


/* =========================================================
   TOP HEADER
   ========================================================= */

header[data-testid="stHeader"] {
    background: rgba(244, 247, 249, 0.94) !important;
    border-bottom: 1px solid rgba(11, 31, 51, 0.06);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

header[data-testid="stHeader"] button {
    color: #0b1f33 !important;
}

header[data-testid="stHeader"] button svg {
    color: #0b1f33 !important;
    fill: #0b1f33 !important;
    stroke: #0b1f33 !important;
}

header[data-testid="stHeader"] button:hover {
    background: rgba(11, 31, 51, 0.07) !important;
}

header[data-testid="stHeader"] button:hover svg {
    color: #0f4c5c !important;
    fill: #0f4c5c !important;
    stroke: #0f4c5c !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0b1f33 0%,
            #0d2a40 55%,
            #091b2c 100%
        );

    border-right: 1px solid #081827;

    box-shadow:
        5px 0 26px rgba(4, 18, 30, 0.10);
}

section[data-testid="stSidebar"] * {
    color: #e8eef3 !important;
}

/* Sidebar navigation */

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 4px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: 9px;
    padding: 7px 9px;
    margin: 1px 0;
    transition:
        background-color 0.15s ease,
        transform 0.15s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.075);
    transform: translateX(2px);
}

section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.93rem;
    color: #e8eef3 !important;
    opacity: 1 !important;
}

section[data-testid="stSidebar"] .stRadio label p,
section[data-testid="stSidebar"] .stRadio label span,
section[data-testid="stSidebar"] .stRadio label div {
    color: #e8eef3 !important;
    -webkit-text-fill-color: #e8eef3 !important;
    opacity: 1 !important;
    visibility: visible !important;
}

/* Sidebar brand */

.brand-mark {
    font-size: 0.70rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #8fb0c3 !important;
    margin-bottom: 0.25rem;
    font-weight: 600;
}

.brand-title {
    font-size: 1.18rem;
    font-weight: 700;
    color: #ffffff !important;
    line-height: 1.3;
    margin-bottom: 1.3rem;
}

/* Sidebar user */

.user-box {
    background: rgba(255, 255, 255, 0.065);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 12px;

    padding: 13px 14px;
    margin-bottom: 18px;

    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.035);
}

.user-box strong {
    display: block;
    font-size: 0.95rem;
    color: #ffffff !important;
}

.user-box span {
    display: block;
    font-size: 0.78rem;
    color: #a9bdcc !important;
    margin-top: 3px;
}


/* =========================================================
   PAGE HEADER
   ========================================================= */

.main-title {
    font-size: 2rem;
    font-weight: 700;
    color: #0b1f33 !important;

    margin: 0 0 0.25rem 0;

    letter-spacing: -0.025em;
    line-height: 1.18;
}

.subtitle {
    color: #526476 !important;
    font-size: 0.98rem;

    margin-bottom: 1.35rem;

    line-height: 1.5;
}

.section-title {
    color: #0b1f33 !important;

    font-size: 1.18rem;
    font-weight: 700;

    margin: 1.45rem 0 0.65rem 0;
}


/* =========================================================
   KPI CARDS
   ========================================================= */

.metric-card {
    position: relative;

    background: #ffffff;

    border: 1px solid #dbe4ea;
    border-radius: 14px;

    padding: 18px 18px 17px 18px;

    min-height: 122px;

    box-shadow:
        0 3px 14px rgba(11, 31, 51, 0.045);

    overflow: hidden;

    transition:
        transform 0.18s ease,
        box-shadow 0.18s ease,
        border-color 0.18s ease;
}

/* Subtle accent line */

.metric-card::before {
    content: "";

    position: absolute;

    top: 0;
    left: 0;
    right: 0;

    height: 3px;

    background: #0f4c5c;
}

.metric-card:hover {
    transform: translateY(-2px);

    border-color: #cbd9e1;

    box-shadow:
        0 8px 24px rgba(11, 31, 51, 0.08);
}

.metric-label {
    color: #536678 !important;

    font-size: 0.72rem;
    font-weight: 700;

    text-transform: uppercase;
    letter-spacing: 0.065em;
}

.metric-value {
    color: #0b1f33 !important;

    font-size: 1.68rem;
    font-weight: 700;

    margin-top: 8px;

    letter-spacing: -0.035em;

    line-height: 1.15;
}

.metric-description {
    color: #718292 !important;

    font-size: 0.78rem;

    margin-top: 7px;

    line-height: 1.35;
}


/* =========================================================
   CHART CONTAINERS
   ========================================================= */

div[data-testid="stPlotlyChart"] {
    background: #ffffff;

    border: 1px solid #dbe4ea;
    border-radius: 13px;

    padding: 7px;

    box-shadow:
        0 3px 14px rgba(11, 31, 51, 0.045);
}


/* =========================================================
   INSIGHTS
   ========================================================= */

.insight-card {
    background: #ffffff;

    border: 1px solid #d8e2e8;
    border-left: 4px solid #0f4c5c;

    border-radius: 10px;

    padding: 14px 18px;

    margin-bottom: 10px;

    box-shadow:
        0 2px 10px rgba(11, 31, 51, 0.035);
}

.insight-title {
    color: #0b1f33 !important;

    font-weight: 700;
    font-size: 0.95rem;

    margin-bottom: 4px;
}

.insight-text {
    color: #405466 !important;

    font-size: 0.9rem;
    line-height: 1.5;
}


/* =========================================================
   INFORMATION BOX
   ========================================================= */

.note-box {
    background:
        linear-gradient(
            135deg,
            #eef6f7,
            #f6f9fa
        );

    border: 1px solid #cfe0e3;

    border-radius: 10px;

    padding: 12px 14px;

    color: #334155 !important;

    font-size: 0.9rem;

    margin: 0.4rem 0 1rem 0;
}


/* =========================================================
   DATAFRAME
   ========================================================= */

div[data-testid="stDataFrame"] {
    border: 1px solid #d8e2e8;

    border-radius: 10px;

    overflow: hidden;

    box-shadow:
        0 2px 10px rgba(11, 31, 51, 0.035);
}


/* =========================================================
   AUTHENTICATION
   ========================================================= */

.auth-wrap {
    max-width: 460px;

    margin: 3.5rem auto 2rem auto;

    background: #ffffff;

    border: 1px solid #dbe4ea;

    border-radius: 18px;

    padding: 2rem 2rem 1.4rem 2rem;

    box-shadow:
        0 16px 45px rgba(11, 31, 51, 0.09);
}

.auth-kicker {
    font-size: 0.75rem;

    letter-spacing: 0.14em;

    text-transform: uppercase;

    color: #0f4c5c !important;

    font-weight: 700;
}

.auth-title {
    font-size: 1.72rem;

    font-weight: 700;

    color: #0b1f33 !important;

    margin: 0.35rem 0 0.4rem 0;
}

.auth-copy {
    color: #536678 !important;

    font-size: 0.95rem;

    margin-bottom: 1.2rem;

    line-height: 1.5;
}

.auth-wrap + div {
    color: #0b1f33 !important;
}


/* =========================================================
   FORM LABELS
   ========================================================= */

div[data-testid="stRadio"] label p {
    color: #0b1f33 !important;

    font-weight: 600 !important;
}

div[data-testid="stRadio"] label {
    color: #0b1f33 !important;
}

div[data-testid="stTextInput"] label p {
    color: #334155 !important;

    font-weight: 600 !important;
}


/* =========================================================
   INPUTS
   ========================================================= */

div[data-testid="stTextInput"] input {
    background-color: #ffffff !important;

    color: #0b1f33 !important;

    border: 1px solid #cbd5e1 !important;

    border-radius: 9px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #0f4c5c !important;

    box-shadow:
        0 0 0 1px #0f4c5c,
        0 0 0 4px rgba(15, 76, 92, 0.08) !important;
}


/* =========================================================
   SELECTBOX / DATE INPUT
   ========================================================= */

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;

    border-color: #cbd5e1 !important;

    border-radius: 9px !important;
}

div[data-baseweb="select"] span {
    color: #0b1f33 !important;
}

div[data-baseweb="select"] input {
    color: #0b1f33 !important;
}

div[data-testid="stDateInput"] input {
    background-color: #ffffff !important;

    color: #0b1f33 !important;

    border-color: #cbd5e1 !important;

    border-radius: 9px !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

div[data-testid="stFormSubmitButton"] button {
    background-color: #0b1f33 !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 9px !important;

    font-weight: 700 !important;

    min-height: 44px !important;

    transition:
        background-color 0.15s ease,
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #123a57 !important;

    color: #ffffff !important;

    transform: translateY(-1px);

    box-shadow:
        0 5px 14px rgba(11, 31, 51, 0.16);
}

div[data-testid="stFormSubmitButton"] button p {
    color: #ffffff !important;

    font-weight: 700 !important;
}

.stDownloadButton button,
.stButton button {
    border-radius: 9px;

    font-weight: 600;
}


/* =========================================================
   GENERAL TEXT
   ========================================================= */

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #263746;
}

[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #0b1f33 !important;
}


/* =========================================================
   STREAMLIT METRICS
   ========================================================= */

[data-testid="stMetricValue"] {
    color: #0b1f33 !important;

    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #536678 !important;
}


/* =========================================================
   ALERTS
   ========================================================= */

div[data-testid="stAlert"] {
    border-radius: 10px;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    color: #657687 !important;

    margin-top: 2.8rem;

    padding-top: 1.2rem;

    border-top: 1px solid #d8e2e8;

    font-size: 0.82rem;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        font-size: 1.55rem;
    }

    .metric-card {
        min-height: 105px;
    }

    .metric-value {
        font-size: 1.45rem;
    }

    .auth-wrap {
        margin-top: 2rem;
        padding: 1.5rem;
    }
}

</style>
"""