"""COVID-19 Pandemic Trend Analysis - authenticated Streamlit application."""

from __future__ import annotations

import html
import sys
from pathlib import Path

import streamlit as st


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =========================================================
# PROJECT IMPORTS
# =========================================================

from auth.auth import authenticate_user, register_user
from dashboard.components.styles import APP_CSS
from dashboard.utils.data_loader import load_all_data
from dashboard.views import (
    render_about,
    render_comparison,
    render_country_analysis,
    render_data_explorer,
    render_global_analysis,
    render_india_analysis,
    render_insights_page,
    render_overview,
    render_peak_analysis,
    render_rankings,
    render_trends,
    render_vaccination,
)
from database.database import init_db, log_activity


# =========================================================
# HTML HELPERS
# =========================================================

def render_html(content: str) -> None:
    """Render multiline HTML on the main page with proper dedenting."""
    # Remove ALL leading whitespace from each line to prevent Markdown code block interpretation
    lines = [line.lstrip() for line in content.split('\n')]
    cleaned = '\n'.join(lines).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_sidebar_html(content: str) -> None:
    """Render multiline HTML in the sidebar with proper dedenting."""
    # Remove ALL leading whitespace from each line to prevent Markdown code block interpretation
    lines = [line.lstrip() for line in content.split('\n')]
    cleaned = '\n'.join(lines).strip()
    st.sidebar.markdown(cleaned, unsafe_allow_html=True)


# =========================================================
# STREAMLIT CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="COVID-19 Pandemic Trend Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# APPLICATION CSS
# =========================================================

st.markdown(
    APP_CSS,
    unsafe_allow_html=True,
)


# =========================================================
# DATABASE
# =========================================================

init_db()


# =========================================================
# DASHBOARD PAGES
# =========================================================

PAGES = [
    "Overview",
    "Global Analysis",
    "Country Analysis",
    "India Analysis",
    "Pandemic Trends",
    "Peak Analysis",
    "Vaccination Analysis",
    "Country Comparison",
    "Country Rankings",
    "Data Explorer",
    "Insights",
    "About",
]


# =========================================================
# SESSION INITIALIZATION
# =========================================================

def _init_session() -> None:
    """Initialize application session state."""

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "auth_mode_selector" not in st.session_state:
        st.session_state.auth_mode_selector = "Sign in"

    if "dashboard_navigation" not in st.session_state:
        st.session_state.dashboard_navigation = "Overview"


# =========================================================
# AUTHENTICATION LANDING PAGE
# =========================================================

def render_auth() -> None:
    """Render the polished medical-tech authentication page."""

    # =====================================================
    # PAGE INTRO / BRAND
    # =====================================================

    render_html(
        """
        <div class="auth-page-shell">

            <div class="auth-brand-row">

                <div class="auth-brand-icon">
                    <span>+</span>
                </div>

                <div>
                    <div class="auth-brand-name">
                        PANDEMIC ANALYTICS
                    </div>

                    <div class="auth-brand-subtitle">
                        Clinical surveillance intelligence
                    </div>
                </div>

            </div>

        </div>
        """
    )

    # =====================================================
    # MAIN AUTHENTICATION LAYOUT
    # =====================================================

    left_col, right_col = st.columns(
        [1.15, 0.85],
        gap="large",
    )

    # =====================================================
    # LEFT MEDICAL-TECH PANEL
    # =====================================================

    with left_col:

        render_html(
            """
            <div class="medical-hero">

                <div class="hero-grid-pattern"></div>

                <div class="hero-content">

                    <div class="hero-status">
                        <span class="live-dot"></span>
                        PANDEMIC SURVEILLANCE PLATFORM
                    </div>

                    <h1 class="medical-title">
                        COVID-19
                        <br>
                        <span>Pandemic Trend Analysis</span>
                    </h1>

                    <p class="medical-copy">
                        Explore global pandemic trends, country-level
                        surveillance, vaccination coverage, peak intensity,
                        comparative analysis and data-driven insights.
                    </p>

                    <div class="medical-feature-list">

                        <div class="medical-feature">
                            <div class="feature-icon">↗</div>

                            <div>
                                <strong>Global surveillance</strong>
                                <span>
                                    Monitor reported pandemic trends
                                </span>
                            </div>
                        </div>

                        <div class="medical-feature">
                            <div class="feature-icon">◎</div>

                            <div>
                                <strong>Country intelligence</strong>
                                <span>
                                    Compare locations and outcomes
                                </span>
                            </div>
                        </div>

                        <div class="medical-feature">
                            <div class="feature-icon">⌁</div>

                            <div>
                                <strong>Data-driven insights</strong>
                                <span>
                                    Identify peaks and emerging patterns
                                </span>
                            </div>
                        </div>

                    </div>

                </div>

                <!-- MEDICAL DATA VISUAL -->

                <div class="medical-visual">

                    <div class="visual-ring ring-one"></div>
                    <div class="visual-ring ring-two"></div>
                    <div class="visual-ring ring-three"></div>

                    <div class="visual-core">

                        <div class="core-cross">
                            +
                        </div>

                        <div class="core-label">
                            COVID
                        </div>

                        <div class="core-small">
                            GLOBAL DATA
                        </div>

                    </div>

                    <div class="data-node node-one">
                        <span class="node-dot"></span>
                        CASES
                    </div>

                    <div class="data-node node-two">
                        <span class="node-dot"></span>
                        TRENDS
                    </div>

                    <div class="data-node node-three">
                        <span class="node-dot"></span>
                        VACCINATION
                    </div>

                    <div class="floating-panel panel-top">

                        <span class="panel-label">
                            GLOBAL STATUS
                        </span>

                        <strong>
                            SURVEILLANCE
                        </strong>

                        <small>
                            Data monitoring active
                        </small>

                    </div>

                    <div class="floating-panel panel-bottom">

                        <div class="mini-chart">

                            <span style="height: 24%"></span>
                            <span style="height: 38%"></span>
                            <span style="height: 31%"></span>
                            <span style="height: 55%"></span>
                            <span style="height: 44%"></span>
                            <span style="height: 70%"></span>
                            <span style="height: 82%"></span>

                        </div>

                        <div class="panel-bottom-text">

                            <strong>
                                Trend intelligence
                            </strong>

                            <small>
                                Multi-country analysis
                            </small>

                        </div>

                    </div>

                </div>

                <div class="hero-footer-line">

                    <span>GLOBAL</span>
                    <span>COUNTRY</span>
                    <span>VACCINATION</span>
                    <span>PEAK ANALYSIS</span>

                </div>

            </div>
            """
        )

    # =====================================================
    # RIGHT AUTHENTICATION PANEL
    # =====================================================

    with right_col:

        render_html(
            """
            <div class="auth-card">

                <div class="auth-account-label">
                    ACCOUNT ACCESS
                </div>

                <h2 class="auth-card-title">
                    Welcome back
                </h2>

                <p class="auth-card-subtitle">
                    Sign in to continue to your analytics workspace.
                </p>

            </div>
            """
        )

        # =================================================
        # AUTH MODE SELECTOR
        # =================================================

        mode = st.radio(
            "Select an option",
            ["Sign in", "Create account"],
            horizontal=True,
            key="auth_mode_selector",
        )

        # =================================================
        # SIGN IN
        # =================================================

        if mode == "Sign in":

            render_html(
                """
                <div class="auth-section-heading">

                    <div class="auth-section-title">
                        Sign in
                    </div>

                    <div class="auth-section-description">
                        Enter your credentials to access the dashboard.
                    </div>

                </div>
                """
            )

            with st.form(
                "login_form",
                clear_on_submit=False,
            ):

                username = st.text_input(
                    "Username",
                    placeholder="Enter your username",
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                )

                submitted = st.form_submit_button(
                    "Sign in to dashboard",
                    width="stretch",
                )

            if submitted:

                username = username.strip()

                ok, message, profile = authenticate_user(
                    username,
                    password,
                )

                if ok:

                    st.session_state.authenticated = True
                    st.session_state.user = profile

                    if profile and profile.get("id") is not None:

                        try:
                            log_activity(
                                profile["id"],
                                "login",
                            )
                        except Exception:
                            pass

                    st.rerun()

                else:

                    st.error(message)

        # =================================================
        # CREATE ACCOUNT
        # =================================================

        else:

            render_html(
                """
                <div class="auth-section-heading">

                    <div class="auth-section-title">
                        Create account
                    </div>

                    <div class="auth-section-description">
                        Set up your account to access the analytics workspace.
                    </div>

                </div>
                """
            )

            with st.form(
                "register_form",
                clear_on_submit=False,
            ):

                full_name = st.text_input(
                    "Full name",
                    placeholder="Enter your full name",
                )

                username = st.text_input(
                    "Username",
                    placeholder="Choose a username",
                )

                email = st.text_input(
                    "Email",
                    placeholder="Enter your email address",
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Minimum 8 characters",
                )

                confirm = st.text_input(
                    "Confirm password",
                    type="password",
                    placeholder="Re-enter your password",
                )

                submitted = st.form_submit_button(
                    "Create account",
                    width="stretch",
                )

            if submitted:

                ok, message = register_user(
                    full_name.strip(),
                    username.strip(),
                    email.strip(),
                    password,
                    confirm,
                )

                if ok:

                    st.success(message)

                    st.session_state.auth_mode_selector = "Sign in"

                    st.rerun()

                else:

                    st.error(message)

        # =================================================
        # SECURITY NOTE
        # =================================================

        render_html(
            """
            <div class="auth-security">

                <div class="security-icon">
                    🔒
                </div>

                <div>

                    <strong>
                        Secure workspace
                    </strong>

                    <span>
                        Your credentials are protected using password hashing.
                    </span>

                </div>

            </div>
            """
        )

        # =================================================
        # AUTH FOOTER
        # =================================================

        render_html(
            """
            <div class="auth-footer">

                <span>
                    COVID-19 Pandemic Trend Analysis
                </span>

                <span class="footer-divider">
                    •
                </span>

                <span>
                    Academic analytics platform
                </span>

            </div>
            """
        )


# =========================================================
# SIDEBAR
# =========================================================

def render_sidebar() -> str:
    """Render the dashboard sidebar."""

    user = st.session_state.user or {}

    full_name = html.escape(
        str(user.get("full_name", "User"))
    )

    username = html.escape(
        str(user.get("username", "user"))
    )

    # =====================================================
    # BRAND
    # =====================================================

    render_sidebar_html(
        """
        <div class="sidebar-brand">

            <div class="sidebar-brand-icon">
                +
            </div>

            <div>

                <div class="sidebar-brand-kicker">
                    SURVEILLANCE
                </div>

                <div class="sidebar-brand-title">
                    COVID-19
                </div>

                <div class="sidebar-brand-subtitle">
                    Pandemic Trend Analysis
                </div>

            </div>

        </div>
        """
    )

    # =====================================================
    # USER PROFILE
    # =====================================================

    initial = (
        full_name.strip()[0].upper()
        if full_name.strip()
        else "U"
    )

    render_sidebar_html(
        f"""
        <div class="sidebar-user-card">

            <div class="user-avatar">
                {html.escape(initial)}
            </div>

            <div class="user-details">

                <strong>
                    {full_name}
                </strong>

                <span>
                    @{username}
                </span>

            </div>

        </div>
        """
    )

    # =====================================================
    # NAVIGATION LABEL
    # =====================================================

    render_sidebar_html(
        """
        <div class="sidebar-section-label">
            NAVIGATION
        </div>
        """
    )

    # =====================================================
    # NAVIGATION
    # =====================================================

    page = st.sidebar.radio(
        "Navigation",
        PAGES,
        key="dashboard_navigation",
        label_visibility="collapsed",
    )



    # =====================================================
    # SIGN OUT
    # =====================================================

    if st.sidebar.button(
        "Sign out",
        width="stretch",
        key="sign_out_button",
    ):

        if user.get("id") is not None:

            try:
                log_activity(
                    user["id"],
                    "logout",
                )
            except Exception:
                pass

        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.auth_mode_selector = "Sign in"

        st.rerun()

    # =====================================================
    # SIDEBAR STATUS
    # =====================================================

    render_sidebar_html(
        """
        <div class="sidebar-status">
            <span class="status-dot"></span>
            Protected workspace - SQLite session
        </div>
        """
    )

    return page


# =========================================================
# DASHBOARD CONTENT
# =========================================================

def render_dashboard(page: str) -> None:
    """Load datasets and render the selected dashboard page."""

    try:

        data = load_all_data()

    except Exception as exc:

        st.error(
            "The dashboard could not load the required datasets."
        )

        st.exception(exc)

        st.stop()

    # =====================================================
    # DATASETS
    # =====================================================

    country_df = data["country"]
    global_df = data["global"]
    peaks_df = data["peaks"]
    vaccination_df = data["vaccination"]

    # =====================================================
    # PAGE ROUTING
    # =====================================================

    if page == "Overview":

        render_overview(
            country_df,
            global_df,
            peaks_df,
        )

    elif page == "Global Analysis":

        render_global_analysis(
            global_df,
        )

    elif page == "Country Analysis":

        render_country_analysis(
            country_df,
            vaccination_df,
        )

    elif page == "India Analysis":

        render_india_analysis(
            country_df,
            global_df,
            peaks_df,
            vaccination_df,
        )

    elif page == "Pandemic Trends":

        render_trends(
            global_df,
        )

    elif page == "Peak Analysis":

        render_peak_analysis(
            peaks_df,
            country_df,
        )

    elif page == "Vaccination Analysis":

        render_vaccination(
            country_df,
            vaccination_df,
        )

    elif page == "Country Comparison":

        render_comparison(
            country_df,
        )

    elif page == "Country Rankings":

        render_rankings(
            country_df,
        )

    elif page == "Data Explorer":

        render_data_explorer(
            country_df,
            global_df,
        )

    elif page == "Insights":

        render_insights_page(
            country_df,
            global_df,
            peaks_df,
        )

    elif page == "About":

        render_about(
            country_df,
            global_df,
        )

    # =====================================================
    # DASHBOARD FOOTER
    # =====================================================

    render_html(
        """
        <div class="dashboard-footer">

            <span>
                COVID-19 Pandemic Trend Analysis
            </span>

            <span class="footer-divider">
                •
            </span>

            <span>
                Reported surveillance data from project CSV files
            </span>

        </div>
        """
    )


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    """Application entry point."""

    _init_session()

    # =====================================================
    # AUTHENTICATION PAGE
    # =====================================================

    if not st.session_state.authenticated:

        render_auth()

        return

    # =====================================================
    # DASHBOARD
    # =====================================================

    page = render_sidebar()

    render_dashboard(page)


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    main()