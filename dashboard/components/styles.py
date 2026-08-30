"""Application visual theme. Original design; not copied from WHO branding."""

APP_CSS = """
<style>

@import url("https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&display=swap");

html, body, [class*="css"] {
    font-family: "Source Sans 3", "Segoe UI", Helvetica, Arial, sans-serif;
}

.stApp {
    background-color: #f3f6f8;
    color: #0b1f33 !important;
}

.block-container {
    max-width: 1280px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

/* ---------- HEADER ---------- */

header[data-testid="stHeader"] {
    background: rgba(243, 246, 248, 0.92);
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: #0b1f33;
    border-right: 1px solid #0a1827;
}

section[data-testid="stSidebar"] * {
    color: #e8eef3 !important;
}

section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.92rem;
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

.brand-mark {
    font-size: 0.72rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8aa4b8 !important;
    margin-bottom: 0.2rem;
}

.brand-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #ffffff !important;
    line-height: 1.3;
    margin-bottom: 1.2rem;
}

.user-box {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 16px;
}

.user-box strong {
    display: block;
    font-size: 0.95rem;
    color: #ffffff !important;
}

.user-box span {
    display: block;
    font-size: 0.78rem;
    color: #9fb3c4 !important;
    margin-top: 2px;
}

/* ---------- PAGE TEXT ---------- */

.main-title {
    font-size: 1.85rem;
    font-weight: 700;
    color: #0b1f33 !important;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.02em;
}

.subtitle {
    color: #5b6b7c !important;
    font-size: 0.98rem;
    margin-bottom: 1.4rem;
}

.section-title {
    color: #0b1f33 !important;
    font-size: 1.2rem;
    font-weight: 700;
    margin: 1.6rem 0 0.7rem 0;
}

/* ---------- KPI CARDS ---------- */

.metric-card {
    background: #ffffff;
    border: 1px solid #dbe4ea;
    border-radius: 12px;
    padding: 18px 18px 16px 18px;
    min-height: 118px;
    box-shadow: 0 1px 2px rgba(11, 31, 51, 0.04);
}

.metric-label {
    color: #5b6b7c !important;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.metric-value {
    color: #0b1f33 !important;
    font-size: 1.65rem;
    font-weight: 700;
    margin-top: 8px;
    letter-spacing: -0.03em;
}

.metric-description {
    color: #7b8b99 !important;
    font-size: 0.78rem;
    margin-top: 6px;
}

/* ---------- CHARTS ---------- */

div[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid #dbe4ea;
    border-radius: 10px;
    padding: 6px;
    box-shadow: 0 1px 3px rgba(11, 31, 51, 0.04);
}

/* ---------- INSIGHTS ---------- */

.insight-card {
    background: #ffffff;
    border: 1px solid #dbe4ea;
    border-left: 4px solid #0f4c5c;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
}

.insight-title {
    color: #0b1f33 !important;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 4px;
}

.insight-text {
    color: #445566 !important;
    font-size: 0.9rem;
    line-height: 1.5;
}

/* ---------- NOTE / ALERT BOX ---------- */

.note-box {
    background: #eef5f6;
    border: 1px solid #cfe0e3;
    border-radius: 8px;
    padding: 12px 14px;
    color: #334155 !important;
    font-size: 0.9rem;
    margin: 0.4rem 0 1rem 0;
}

/* ---------- DATAFRAME ---------- */

div[data-testid="stDataFrame"] {
    border: 1px solid #dbe4ea;
    border-radius: 8px;
}

/* ---------- AUTHENTICATION ---------- */

.auth-wrap {
    max-width: 460px;
    margin: 3.5rem auto 2rem auto;
    background: #ffffff;
    border: 1px solid #dbe4ea;
    border-radius: 16px;
    padding: 2rem 2rem 1.4rem 2rem;
    box-shadow: 0 12px 40px rgba(11, 31, 51, 0.08);
}

.auth-kicker {
    font-size: 0.75rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #0f4c5c !important;
    font-weight: 700;
}

.auth-title {
    font-size: 1.7rem;
    font-weight: 700;
    color: #0b1f33 !important;
    margin: 0.35rem 0 0.4rem 0;
}

.auth-copy {
    color: #5b6b7c !important;
    font-size: 0.95rem;
    margin-bottom: 1.2rem;
}

.auth-wrap + div {
    color: #0b1f33 !important;
}

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

div[data-testid="stTextInput"] input {
    background-color: #ffffff !important;
    color: #0b1f33 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #0f4c5c !important;
    box-shadow: 0 0 0 1px #0f4c5c !important;
}

/* ---------- BUTTONS ---------- */

div[data-testid="stFormSubmitButton"] button {
    background-color: #0b1f33 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    min-height: 44px !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background-color: #123a57 !important;
    color: #ffffff !important;
}

div[data-testid="stFormSubmitButton"] button p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.stDownloadButton button,
.stButton button {
    border-radius: 8px;
    font-weight: 600;
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #7b8b99 !important;
    margin-top: 2.8rem;
    padding-top: 1.2rem;
    border-top: 1px solid #dbe4ea;
    font-size: 0.82rem;
}

/* ---------- STREAMLIT TEXT SAFETY ---------- */

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #263746;
}

[data-testid="stMetricValue"] {
    color: #0b1f33 !important;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #5b6b7c !important;
}

</style>
"""
