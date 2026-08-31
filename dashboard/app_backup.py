"""COVID-19 Pandemic Trend Analysis - authenticated Streamlit application."""

from __future__ import annotations

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
# STREAMLIT CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="COVID-19 Pandemic Trend Analysis",
    page_icon="C",
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
    """Initialize authentication-related session state."""

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"


# =========================================================
# AUTHENTICATION LANDING PAGE
# =========================================================

def render_auth() -> None:
    """Render the authentication landing page."""

    # =====================================================
    # HERO SECTION
    # =====================================================

    st.markdown(
        """
        <div class="auth-hero">

            <div class="auth-hero-left">

                <div class="auth-kicker">
                    ACADEMIC ANALYTICS
                </div>

                <div class="auth-title">
                    COVID-19 Pandemic<br>
                    Trend Analysis
                </div>

                <div class="auth-copy">
                    Explore global pandemic trends, country comparisons,
                    vaccination coverage, peak analysis and data-driven insights.
                </div>

                <div class="auth-feature-row">
                    <span>Global trends</span>
                    <span>Country analysis</span>
                    <span>Data insights</span>
                </div>

            </div>

            <div class="auth-visual">

                <div class="visual-orbit orbit-one"></div>
                <div class="visual-orbit orbit-two"></div>

                <div class="visual-globe">
                    COVID
                </div>

                <div class="visual-card visual-card-top">

                    <span class="visual-card-label">
                        GLOBAL
                    </span>

                    <strong>
                        COVID-19
                    </strong>

                    <small>
                        Surveillance
                    </small>

                </div>

                <div class="visual-card visual-card-bottom">

                    <span class="visual-bar bar-one"></span>
                    <span class="visual-bar bar-two"></span>
                    <span class="visual-bar bar-three"></span>
                    <span class="visual-bar bar-four"></span>
                    <span class="visual-bar bar-five"></span>

                    <div>
                        <strong>
                            Trend analysis
                        </strong>

                        <small>
                            Data-driven insights
                        </small>
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # AUTHENTICATION AREA
    # =====================================================

    left_col, right_col = st.columns(
        [0.82, 1.18],
        gap="large",
    )


    # =====================================================
    # LEFT SIDE
    # =====================================================

    with left_col:

        st.markdown(
            """
            <div class="auth-intro">

                <div class="form-heading">
                    Welcome back
                </div>

                <div class="form-subheading">
                    Sign in to continue to your dashboard.
                </div>

                <div class="auth-account-label">
                    ACCOUNT
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        mode = st.radio(
            "Account",
            ["Sign in", "Create account"],
            horizontal=True,
            label_visibility="collapsed",
            key="auth_mode_selector",
        )


        st.markdown(
            """
            <div class="auth-helper">
                Secure access to your COVID-19 analytics workspace.
            </div>
            """,
            unsafe_allow_html=True,
        )


    # =====================================================
    # RIGHT SIDE
    # =====================================================

    with right_col:

        # =================================================
        # LOGIN FORM
        # =================================================

        if mode == "Sign in":

            st.markdown(
                """
                <div class="auth-form-card">

                    <div class="form-heading">
                        Sign in
                    </div>

                    <div class="form-subheading">
                        Enter your credentials to continue.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
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
                    "Sign in",
                    width="stretch",
                )


            if submitted:

                ok, message, profile = authenticate_user(
                    username,
                    password,
                )

                if ok:

                    st.session_state.authenticated = True
                    st.session_state.user = profile

                    st.rerun()

                else:

                    st.error(message)


        # =================================================
        # REGISTRATION FORM
        # =================================================

        else:

            st.markdown(
                """
                <div class="auth-form-card">

                    <div class="form-heading">
                        Create your account
                    </div>

                    <div class="form-subheading">
                        Set up your account to access the analytics dashboard.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
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
                    full_name,
                    username,
                    email,
                    password,
                    confirm,
                )

                if ok:

                    st.success(message)

                else:

                    st.error(message)


    # =====================================================
    # SECURITY MESSAGE
    # =====================================================

    st.markdown(
        """
        <div class="auth-security">
            ðŸ”’ Your account credentials are securely stored
            using password hashing.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # FOOTER
    # =====================================================

    st.markdown(
        """
        <div class="footer">
            COVID-19 Pandemic Trend Analysis -
            Academic demonstration application
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================

def render_sidebar() -> str:
    """Render the dashboard sidebar and return the selected page."""

    user = st.session_state.user or {}


    # =====================================================
    # BRAND
    # =====================================================

    st.sidebar.markdown(
        """
        <div class="brand-mark">
            SURVEILLANCE DASHBOARD
        </div>

        <div class="brand-title">
            COVID-19 Pandemic<br>
            Trend Analysis
        </div>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # USER
    # =====================================================

    st.sidebar.markdown(
        f"""
        <div class="user-box">

            <strong>
                {user.get("full_name", "")}
            </strong>

            <span>
                @{user.get("username", "")}
            </span>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # =====================================================
    # NAVIGATION
    # =====================================================

    page = st.sidebar.radio(
        "Navigation",
        PAGES,
        key="dashboard_navigation",
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

            log_activity(
                user["id"],
                "logout",
            )

        st.session_state.authenticated = False
        st.session_state.user = None

        st.rerun()


    # =====================================================
    # SIDEBAR STATUS
    # =====================================================

    st.sidebar.markdown(
        """
        <div class="sidebar-status">

            <span class="status-dot"></span>

            Protected workspace - SQLite session

        </div>
        """,
        unsafe_allow_html=True,
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
    # OVERVIEW
    # =====================================================

    if page == "Overview":

        render_overview(
            country_df,
            global_df,
            peaks_df,
        )


    # =====================================================
    # GLOBAL ANALYSIS
    # =====================================================

    elif page == "Global Analysis":

        render_global_analysis(
            global_df,
        )


    # =====================================================
    # COUNTRY ANALYSIS
    # =====================================================

    elif page == "Country Analysis":

        render_country_analysis(
            country_df,
            vaccination_df,
        )


    # =====================================================
    # INDIA ANALYSIS
    # =====================================================

    elif page == "India Analysis":

        render_india_analysis(
            country_df,
            global_df,
            peaks_df,
            vaccination_df,
        )


    # =====================================================
    # PANDEMIC TRENDS
    # =====================================================

    elif page == "Pandemic Trends":

        render_trends(
            global_df,
        )


    # =====================================================
    # PEAK ANALYSIS
    # =====================================================

    elif page == "Peak Analysis":

        render_peak_analysis(
            peaks_df,
            country_df,
        )


    # =====================================================
    # VACCINATION
    # =====================================================

    elif page == "Vaccination Analysis":

        render_vaccination(
            country_df,
            vaccination_df,
        )


    # =====================================================
    # COUNTRY COMPARISON
    # =====================================================

    elif page == "Country Comparison":

        render_comparison(
            country_df,
        )


    # =====================================================
    # COUNTRY RANKINGS
    # =====================================================

    elif page == "Country Rankings":

        render_rankings(
            country_df,
        )


    # =====================================================
    # DATA EXPLORER
    # =====================================================

    elif page == "Data Explorer":

        render_data_explorer(
            country_df,
            global_df,
        )


    # =====================================================
    # INSIGHTS
    # =====================================================

    elif page == "Insights":

        render_insights_page(
            country_df,
            global_df,
            peaks_df,
        )


    # =====================================================
    # ABOUT
    # =====================================================

    else:

        render_about(
            country_df,
            global_df,
        )


    # =====================================================
    # DASHBOARD FOOTER
    # =====================================================

    st.markdown(
        """
        <div class="footer">
            COVID-19 Pandemic Trend Analysis -
            Reported surveillance data from project CSV files
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# MAIN
# =========================================================

def main() -> None:
    """Application entry point."""

    _init_session()


    # =====================================================
    # NOT AUTHENTICATED
    # =====================================================

    if not st.session_state.authenticated:

        render_auth()

        return


    # =====================================================
    # AUTHENTICATED
    # =====================================================

    page = render_sidebar()

    render_dashboard(page)


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    main()

