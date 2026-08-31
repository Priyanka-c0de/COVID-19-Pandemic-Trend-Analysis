"""Application visual theme for the COVID-19 dashboard."""

APP_CSS = """
<style>

/* =========================================================
   GLOBAL
   ========================================================= */

html,
body,
[class*="css"] {
    font-family:
        "Segoe UI",
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        sans-serif;
}

.stApp {
    background: #f5f8fa !important;
    color: #102a43 !important;
}

.block-container {
    max-width: 1380px !important;
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
}


/* =========================================================
   HIDE STREAMLIT DEFAULT UI
   ========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}


/* =========================================================
   AUTHENTICATION PAGE
   ========================================================= */

.auth-page-shell {
    max-width: 1260px;
    margin: 0 auto 1.4rem auto;
}

.auth-brand-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.2rem 0 0.8rem 0;
}

.auth-brand-icon {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: #0b7285;
    color: #ffffff !important;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(11,114,133,0.18);
}

.auth-brand-name {
    color: #153b50 !important;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.13em;
}

.auth-brand-subtitle {
    color: #78909c !important;
    font-size: 0.68rem;
    margin-top: 1px;
}


/* =========================================================
   MEDICAL HERO
   ========================================================= */

.medical-hero {
    min-height: 690px;
    position: relative;
    overflow: hidden;

    border-radius: 26px;

    background:
        radial-gradient(
            circle at 80% 20%,
            rgba(77, 208, 225, 0.14),
            transparent 28%
        ),
        radial-gradient(
            circle at 20% 85%,
            rgba(38, 166, 154, 0.10),
            transparent 30%
        ),
        linear-gradient(
            145deg,
            #062b3a 0%,
            #073c4b 48%,
            #075363 100%
        );

    box-shadow:
        0 24px 60px rgba(12, 48, 63, 0.16);
}


/* =========================================================
   HERO GRID
   ========================================================= */

.hero-grid-pattern {
    position: absolute;
    inset: 0;

    background-image:
        linear-gradient(
            rgba(255,255,255,0.035) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(255,255,255,0.035) 1px,
            transparent 1px
        );

    background-size: 34px 34px;

    mask-image:
        linear-gradient(
            to bottom,
            rgba(0,0,0,0.7),
            transparent 90%
        );

    pointer-events: none;
}


/* =========================================================
   HERO CONTENT
   ========================================================= */

.hero-content {
    position: relative;
    z-index: 5;

    padding:
        3.1rem
        3.1rem
        1.5rem
        3.1rem;

    max-width: 620px;
}

.hero-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;

    color: #9ce9e1 !important;

    font-size: 0.66rem;
    font-weight: 800;
    letter-spacing: 0.15em;

    margin-bottom: 1.4rem;
}

.live-dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #70e1d4;

    box-shadow:
        0 0 0 5px rgba(112,225,212,0.10);
}

.medical-title {
    margin: 0 0 1.25rem 0 !important;

    color: #ffffff !important;

    font-size: clamp(2.5rem, 4vw, 4.25rem) !important;
    font-weight: 750 !important;

    line-height: 0.98 !important;
    letter-spacing: -0.045em !important;
}

.medical-title span {
    color: #b9eee7 !important;
}

.medical-copy {
    max-width: 540px;

    color: #c3dce3 !important;

    font-size: 0.95rem;
    line-height: 1.7;

    margin: 0;
}


/* =========================================================
   MEDICAL FEATURES
   ========================================================= */

.medical-feature-list {
    margin-top: 2rem;

    display: flex;
    flex-direction: column;
    gap: 11px;
}

.medical-feature {
    display: flex;
    align-items: center;
    gap: 12px;

    width: fit-content;
}

.feature-icon {
    width: 30px;
    height: 30px;

    border-radius: 9px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(113, 225, 212, 0.10);

    border: 1px solid rgba(153, 246, 228, 0.18);

    color: #82e5da !important;

    font-size: 0.9rem;
    font-weight: 700;
}

.medical-feature strong {
    display: block;

    color: #ffffff !important;

    font-size: 0.78rem;
    font-weight: 700;
}

.medical-feature span {
    display: block;

    color: #91b8c4 !important;

    font-size: 0.67rem;

    margin-top: 2px;
}


/* =========================================================
   CENTRAL MEDICAL VISUAL
   ========================================================= */

.medical-visual {
    position: absolute;

    width: 410px;
    height: 410px;

    right: 5%;
    top: 40%;

    transform: translateY(-50%);

    display: flex;
    align-items: center;
    justify-content: center;
}


/* =========================================================
   VISUAL RINGS
   ========================================================= */

.visual-ring {
    position: absolute;

    border-radius: 50%;

    border: 1px solid rgba(150, 241, 231, 0.17);
}

.ring-one {
    width: 330px;
    height: 330px;
}

.ring-two {
    width: 250px;
    height: 250px;

    border-style: dashed;
}

.ring-three {
    width: 180px;
    height: 180px;

    border-color: rgba(150, 241, 231, 0.28);
}


/* =========================================================
   CORE
   ========================================================= */

.visual-core {
    position: relative;
    z-index: 10;

    width: 135px;
    height: 135px;

    border-radius: 50%;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    background:
        radial-gradient(
            circle at 35% 30%,
            rgba(117, 234, 222, 0.22),
            rgba(4, 52, 65, 0.96) 65%
        );

    border:
        1px solid rgba(156, 246, 235, 0.35);

    box-shadow:
        0 0 0 14px rgba(96, 218, 207, 0.035),
        0 0 45px rgba(96, 218, 207, 0.12);
}

.core-cross {
    width: 27px;
    height: 27px;

    border-radius: 8px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: rgba(112, 225, 212, 0.15);

    color: #86e8df !important;

    font-size: 1.15rem;
    font-weight: 800;

    margin-bottom: 7px;
}

.core-label {
    color: #ffffff !important;

    font-size: 0.88rem;
    font-weight: 800;

    letter-spacing: 0.12em;
}

.core-small {
    color: #7fb7c1 !important;

    font-size: 0.52rem;
    letter-spacing: 0.16em;

    margin-top: 3px;
}


/* =========================================================
   DATA NODES
   ========================================================= */

.data-node {
    position: absolute;
    z-index: 12;

    padding: 7px 10px;

    border-radius: 999px;

    background: rgba(3, 43, 55, 0.82);

    border: 1px solid rgba(147, 239, 230, 0.16);

    color: #b7dfe1 !important;

    font-size: 0.53rem;
    font-weight: 700;
    letter-spacing: 0.08em;

    backdrop-filter: blur(8px);
}

.node-dot {
    display: inline-block;

    width: 5px;
    height: 5px;

    border-radius: 50%;

    background: #72dfd1;

    margin-right: 5px;
}

.node-one {
    top: 57px;
    left: 40px;
}

.node-two {
    top: 28px;
    right: 55px;
}

.node-three {
    bottom: 65px;
    right: 15px;
}


/* =========================================================
   FLOATING PANELS
   ========================================================= */

.floating-panel {
    position: absolute;
    z-index: 20;

    background: rgba(8, 53, 66, 0.88);

    border: 1px solid rgba(169, 242, 233, 0.16);

    border-radius: 13px;

    box-shadow:
        0 15px 35px rgba(0,0,0,0.16);

    backdrop-filter: blur(12px);
}

.panel-top {
    top: 28px;
    right: -18px;

    min-width: 145px;

    padding: 12px 14px;
}

.panel-label {
    display: block;

    color: #73dcd1 !important;

    font-size: 0.51rem;
    font-weight: 800;

    letter-spacing: 0.12em;
}

.panel-top strong {
    display: block;

    color: #ffffff !important;

    font-size: 0.76rem;

    margin-top: 5px;
}

.panel-top small {
    display: block;

    color: #91bbc3 !important;

    font-size: 0.58rem;

    margin-top: 2px;
}


/* =========================================================
   MINI CHART PANEL
   ========================================================= */

.panel-bottom {
    left: 0;
    bottom: 28px;

    min-width: 220px;

    padding: 13px;

    display: flex;
    align-items: center;
    gap: 12px;
}

.mini-chart {
    height: 42px;

    display: flex;
    align-items: end;
    gap: 4px;
}

.mini-chart span {
    width: 5px;

    border-radius: 4px 4px 2px 2px;

    background: #66d8ce;
    opacity: 0.82;
}

.panel-bottom-text strong {
    display: block;

    color: #ffffff !important;

    font-size: 0.69rem;
}

.panel-bottom-text small {
    display: block;

    color: #8fb9c2 !important;

    font-size: 0.57rem;

    margin-top: 2px;
}


/* =========================================================
   HERO FOOTER
   ========================================================= */

.hero-footer-line {
    position: absolute;

    bottom: 0;
    left: 0;
    right: 0;

    z-index: 10;

    padding:
        14px
        3.1rem;

    display: flex;
    gap: 24px;

    border-top:
        1px solid rgba(255,255,255,0.08);

    color: #73aab5 !important;

    font-size: 0.53rem;
    font-weight: 800;
    letter-spacing: 0.12em;
}


/* =========================================================
   AUTH CARD
   ========================================================= */

.auth-card {
    padding:
        2.3rem
        2.3rem
        1rem
        2.3rem;
}

.auth-account-label {
    color: #0b8f83 !important;

    font-size: 0.64rem;
    font-weight: 800;

    letter-spacing: 0.15em;

    margin-bottom: 0.65rem;
}

.auth-card-title {
    color: #143b50 !important;

    font-size: 2.15rem !important;
    font-weight: 750 !important;

    letter-spacing: -0.035em !important;

    margin: 0 !important;
}

.auth-card-subtitle {
    color: #718895 !important;

    font-size: 0.85rem;

    line-height: 1.55;

    margin-top: 0.55rem;
}


/* =========================================================
   AUTH SELECTOR
   ========================================================= */

/*
   This is intentionally NOT hidden.

   The radio is transformed into a visible segmented
   control so "Sign in" and "Create account" are obvious.
*/

div[data-testid="stRadio"] {
    margin:
        0.5rem
        2.3rem
        1.5rem
        2.3rem;
}

div[data-testid="stRadio"] > label {
    color: #667d89 !important;

    font-size: 0.62rem !important;
    font-weight: 800 !important;

    text-transform: uppercase;

    letter-spacing: 0.12em;

    margin-bottom: 0.5rem !important;
}

div[data-testid="stRadio"] > div {
    display: flex !important;

    flex-direction: row !important;

    width: 100% !important;

    gap: 0 !important;

    background: #edf3f5;

    border: 1px solid #d7e3e7;

    border-radius: 11px;

    padding: 4px;
}

div[data-testid="stRadio"] > div > label {
    flex: 1 !important;

    min-height: 42px;

    justify-content: center !important;

    border-radius: 8px;

    padding: 8px 12px !important;

    transition: all 0.15s ease;
}

div[data-testid="stRadio"] > div > label p {
    color: #55707d !important;

    font-size: 0.75rem !important;
    font-weight: 700 !important;
}

div[data-testid="stRadio"] > div > label:has(input:checked) {
    background: #ffffff !important;

    box-shadow:
        0 3px 10px rgba(20,59,80,0.10);
}

div[data-testid="stRadio"] > div > label:has(input:checked) p {
    color: #075f70 !important;
}


/* =========================================================
   AUTH SECTION
   ========================================================= */

.auth-section-heading {
    padding:
        0
        2.3rem
        0.8rem
        2.3rem;
}

.auth-section-title {
    color: #173e52 !important;

    font-size: 1.22rem;

    font-weight: 750;
}

.auth-section-description {
    color: #7a8f99 !important;

    font-size: 0.74rem;

    margin-top: 3px;
}


/* =========================================================
   FORM
   ========================================================= */

div[data-testid="stForm"] {
    background: #ffffff !important;

    border:
        1px solid #dce7eb !important;

    border-radius: 17px !important;

    padding: 1.5rem !important;

    margin:
        0
        2.3rem !important;

    box-shadow:
        0 14px 35px rgba(21,59,80,0.07) !important;
}


/* =========================================================
   FORM LABELS
   ========================================================= */

div[data-testid="stTextInput"] label {
    color: #365565 !important;

    font-size: 0.71rem !important;

    font-weight: 700 !important;
}

div[data-testid="stTextInput"] input {
    background: #fbfdfe !important;

    color: #173e52 !important;

    border:
        1px solid #ccdce2 !important;

    border-radius: 9px !important;

    min-height: 42px !important;

    font-size: 0.83rem !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #9aacb5 !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #37a99c !important;

    box-shadow:
        0 0 0 3px rgba(55,169,156,0.10) !important;
}


/* =========================================================
   SUBMIT BUTTON
   ========================================================= */

div[data-testid="stFormSubmitButton"] button {
    min-height: 44px !important;

    background:
        linear-gradient(
            135deg,
            #087f8c,
            #096b78
        ) !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 9px !important;

    font-size: 0.78rem !important;

    font-weight: 750 !important;

    box-shadow:
        0 7px 18px rgba(8,127,140,0.18) !important;
}

div[data-testid="stFormSubmitButton"] button:hover {
    background:
        linear-gradient(
            135deg,
            #076e79,
            #075e6a
        ) !important;
}


/* =========================================================
   SECURITY
   ========================================================= */

.auth-security {
    margin:
        1.2rem
        2.3rem
        0
        2.3rem;

    padding: 11px 13px;

    display: flex;
    align-items: center;

    gap: 10px;

    background: #f0f8f7;

    border:
        1px solid #d4ebe8;

    border-radius: 10px;
}

.security-icon {
    font-size: 0.9rem;
}

.auth-security strong {
    display: block;

    color: #315c62 !important;

    font-size: 0.66rem;
}

.auth-security span {
    display: block;

    color: #759097 !important;

    font-size: 0.57rem;

    margin-top: 2px;
}


/* =========================================================
   AUTH FOOTER
   ========================================================= */

.auth-footer {
    padding:
        1.4rem
        2.3rem;

    color: #91a1a8 !important;

    font-size: 0.61rem;

    text-align: center;
}

.auth-footer span {
    color: #81949d !important;
}

.footer-divider {
    margin: 0 7px;

    color: #b6c4c9 !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #092b3a 0%,
            #082531 100%
        ) !important;

    border-right:
        1px solid rgba(255,255,255,0.06);
}

section[data-testid="stSidebar"] * {
    box-sizing: border-box;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #d9e8ec !important;
}


/* =========================================================
   SIDEBAR BRAND
   ========================================================= */

.sidebar-brand {
    display: flex;

    align-items: center;

    gap: 11px;

    padding:
        0.4rem
        0.2rem
        1.4rem
        0.2rem;

    border-bottom:
        1px solid rgba(255,255,255,0.07);
}

.sidebar-brand-icon {
    width: 34px;
    height: 34px;

    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 9px;

    background: rgba(102,216,206,0.12);

    border:
        1px solid rgba(102,216,206,0.22);

    color: #7de1d7 !important;

    font-size: 1.2rem;
    font-weight: 700;
}

.sidebar-brand-kicker {
    color: #69c9c1 !important;

    font-size: 0.53rem;
    font-weight: 800;

    letter-spacing: 0.15em;
}

.sidebar-brand-title {
    color: #ffffff !important;

    font-size: 1rem;
    font-weight: 750;

    margin-top: 1px;
}

.sidebar-brand-subtitle {
    color: #799da8 !important;

    font-size: 0.58rem;

    margin-top: 2px;
}


/* =========================================================
   SIDEBAR USER
   ========================================================= */

.sidebar-user-card {
    display: flex;

    align-items: center;

    gap: 10px;

    padding:
        1rem
        0.2rem;

    border-bottom:
        1px solid rgba(255,255,255,0.06);
}

.user-avatar {
    width: 35px;
    height: 35px;

    border-radius: 50%;

    flex-shrink: 0;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #d9f1ee;

    color: #096b70 !important;

    font-size: 0.78rem;
    font-weight: 800;
}

.user-details {
    min-width: 0;
}

.user-details strong {
    display: block;

    color: #ffffff !important;

    font-size: 0.72rem;
    font-weight: 700;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.user-details span {
    display: block;

    color: #7fa3ad !important;

    font-size: 0.6rem;

    margin-top: 2px;
}


/* =========================================================
   SIDEBAR NAVIGATION
   ========================================================= */

.sidebar-section-label {
    color: #638a95 !important;

    font-size: 0.54rem;
    font-weight: 800;

    letter-spacing: 0.15em;

    padding:
        1.3rem
        0.2rem
        0.45rem;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] {
    margin: 0 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] > label {
    display: none !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] > div {
    display: flex !important;

    flex-direction: column !important;

    gap: 3px !important;

    background: transparent !important;

    border: none !important;

    padding: 0 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] > div > label {
    min-height: 38px;

    width: 100% !important;

    display: flex !important;

    align-items: center !important;

    justify-content: flex-start !important;

    border-radius: 8px;

    padding:
        7px
        10px !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] > div > label p {
    color: #94b2ba !important;

    font-size: 0.7rem !important;

    font-weight: 600 !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] > div > label:hover {
    background: rgba(255,255,255,0.045);
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] > div > label:has(input:checked) {
    background:
        rgba(102,216,206,0.12) !important;

    border-left:
        3px solid #66d8ce;

    padding-left: 7px !important;
}

section[data-testid="stSidebar"]
div[data-testid="stRadio"] > div > label:has(input:checked) p {
    color: #ffffff !important;

    font-weight: 750 !important;
}


/* =========================================================
   SIDEBAR STATUS
   ========================================================= */

.sidebar-bottom {
    margin-top: 1.2rem;
}

.sidebar-protected {
    display: flex;

    align-items: center;

    gap: 7px;

    padding:
        9px
        8px;

    border-top:
        1px solid rgba(255,255,255,0.06);

    color: #759ba5 !important;

    font-size: 0.59rem;
}

.status-dot {
    width: 6px;
    height: 6px;

    border-radius: 50%;

    background: #69d8cc;

    box-shadow:
        0 0 0 4px rgba(105,216,204,0.08);
}


/* =========================================================
   SIDEBAR STATUS
   ========================================================= */

.sidebar-status {
    display: flex;

    align-items: center;

    gap: 7px;

    padding:
        10px
        8px;

    margin-top: 1.2rem;

    border-top:
        1px solid rgba(255,255,255,0.06);

    border-bottom:
        1px solid rgba(255,255,255,0.06);

    color: #7fb8c1 !important;

    font-size: 0.60rem;

    font-weight: 600;

    letter-spacing: 0.05em;
}


/* =========================================================
   SIDEBAR SIGN OUT
   ========================================================= */

section[data-testid="stSidebar"]
button {
    border-radius: 8px !important;

    min-height: 36px !important;

    color: #a7c0c7 !important;

    background:
        rgba(255,255,255,0.035) !important;

    border:
        1px solid rgba(255,255,255,0.08) !important;
}

section[data-testid="stSidebar"]
button:hover {
    color: #ffffff !important;

    border-color:
        rgba(102,216,206,0.25) !important;
}


/* =========================================================
   MAIN DASHBOARD HEADINGS
   ========================================================= */

.main-title {
    color: #143b50 !important;

    font-size: 2rem;

    font-weight: 750;
}

.subtitle {
    color: #607985 !important;

    font-size: 0.92rem;
}

.section-title {
    color: #143b50 !important;

    font-size: 1.15rem;

    font-weight: 750;
}


/* =========================================================
   DASHBOARD CARDS
   ========================================================= */

.metric-card {
    background: #ffffff;

    border:
        1px solid #dce7eb;

    border-radius: 14px;

    padding: 18px;

    box-shadow:
        0 5px 18px rgba(20,59,80,0.045);
}

.metric-label {
    color: #67808b !important;

    font-size: 0.68rem;

    font-weight: 800;

    letter-spacing: 0.06em;
}

.metric-value {
    color: #123d51 !important;

    font-size: 1.68rem;

    font-weight: 750;
}

.metric-description {
    color: #82949c !important;

    font-size: 0.73rem;
}


/* =========================================================
   INSIGHT CARDS
   ========================================================= */

.insight-card {
    background: #ffffff;

    border:
        1px solid #dce7eb;

    border-left:
        4px solid #159a91;

    border-radius: 11px;

    padding: 14px 18px;

    box-shadow:
        0 4px 15px rgba(20,59,80,0.035);
}

.insight-title {
    color: #173e52 !important;

    font-weight: 750;
}

.insight-text {
    color: #536c78 !important;
}


/* =========================================================
   NOTE BOX
   ========================================================= */

.note-box {
    background: #eff8f7;

    border:
        1px solid #d3ebe7;

    border-radius: 10px;

    padding: 12px 14px;

    color: #46636c !important;
}


/* =========================================================
   DASHBOARD FOOTER
   ========================================================= */

.dashboard-footer {
    max-width: 1120px;

    margin:
        2.2rem auto 0 auto;

    padding-top: 1rem;

    border-top:
        1px solid #dce7eb;

    text-align: center;

    color: #82939b !important;

    font-size: 0.65rem;
}

.dashboard-footer span {
    color: #82939b !important;
}

.dashboard-footer .footer-divider {
    margin: 0 8px;

    color: #b5c1c6 !important;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 1100px) {

    .medical-visual {
        opacity: 0.55;

        right: -5%;
    }

    .hero-content {
        max-width: 570px;
    }

}


@media (max-width: 900px) {

    .medical-hero {
        min-height: 760px;
    }

    .medical-visual {
        position: absolute;

        width: 340px;
        height: 340px;

        top: auto;
        bottom: 50px;
        right: 50%;

        transform: translateX(50%);

        opacity: 0.7;
    }

    .hero-content {
        padding: 2.2rem;
    }

    .medical-title {
        font-size: 3rem !important;
    }

    .hero-footer-line {
        padding-left: 2.2rem;
        padding-right: 2.2rem;

        gap: 12px;
    }

}


@media (max-width: 700px) {

    .medical-hero {
        min-height: 800px;

        border-radius: 20px;
    }

    .hero-content {
        padding: 1.7rem;
    }

    .medical-title {
        font-size: 2.5rem !important;
    }

    .medical-copy {
        font-size: 0.82rem;
    }

    .medical-visual {
        width: 300px;
        height: 300px;

        bottom: 65px;
    }

    .floating-panel {
        transform: scale(0.85);
    }

    .hero-footer-line {
        display: none;
    }

    .auth-card {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    div[data-testid="stRadio"] {
        margin-left: 1rem;
        margin-right: 1rem;
    }

    .auth-section-heading {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    div[data-testid="stForm"] {
        margin-left: 1rem !important;
        margin-right: 1rem !important;
    }

    .auth-security {
        margin-left: 1rem;
        margin-right: 1rem;
    }

    .auth-footer {
        padding-left: 1rem;
        padding-right: 1rem;
    }

}

</style>
"""