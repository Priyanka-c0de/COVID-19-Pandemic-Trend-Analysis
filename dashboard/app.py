"""COVID-19 Pandemic Trend Analysis — authenticated Streamlit application."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

st.set_page_config(
    page_title="COVID-19 Pandemic Trend Analysis",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(APP_CSS, unsafe_allow_html=True)
init_db()

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


def _init_session() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"


def render_auth() -> None:
    st.markdown(
        """
        <div class="auth-page">
            <div class="auth-card">
                <div class="auth-kicker">ACADEMIC ANALYTICS</div>
                <div class="auth-title">COVID-19 Pandemic<br/>Trend Analysis</div>
                <div class="auth-copy">
                    Explore pandemic trends, country comparisons, vaccination coverage,
                    peak analysis and data-driven insights.
                </div>
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
    )

    st.markdown('<div class="auth-form-wrap">', unsafe_allow_html=True)

    if mode == "Sign in":
        st.markdown(
            '<div class="form-heading">Welcome back</div>'
            '<div class="form-subheading">Sign in to continue to your dashboard.</div>',
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
            )
            submitted = st.form_submit_button("Sign in", width="stretch")

        if submitted:
            ok, message, profile = authenticate_user(username, password)
            if ok:
                st.session_state.authenticated = True
                st.session_state.user = profile
                st.rerun()
            else:
                st.error(message)

    else:
        st.markdown(
            '<div class="form-heading">Create your account</div>'
            '<div class="form-subheading">Set up your account to access the analytics dashboard.</div>',
            unsafe_allow_html=True,
        )

        with st.form("register_form", clear_on_submit=False):
            full_name = st.text_input("Full name", placeholder="Enter your full name")
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email address")
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
            submitted = st.form_submit_button("Create account", width="stretch")

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

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="auth-security">🔒 Your account credentials are securely stored using password hashing.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="footer">COVID-19 Pandemic Trend Analysis · Academic demonstration application</div>',
        unsafe_allow_html=True,
    )

def render_sidebar() -> str:
    user = st.session_state.user or {}
    st.sidebar.markdown(
        """
        <div class="brand-mark">Surveillance dashboard</div>
        <div class="brand-title">COVID-19 Pandemic<br/>Trend Analysis</div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f"""
        <div class="user-box">
            <strong>{user.get("full_name", "")}</strong>
            <span>@{user.get("username", "")}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.sidebar.radio("Navigation", PAGES)
    if st.sidebar.button("Sign out", width="stretch"):
        if user.get("id") is not None:
            log_activity(user["id"], "logout")
        st.session_state.authenticated = False
        st.session_state.user = None
        st.rerun()
    st.sidebar.caption("Protected workspace · SQLite session")
    return page


def render_dashboard(page: str) -> None:
    try:
        data = load_all_data()
    except Exception as exc:
        st.error("The dashboard could not load the required datasets.")
        st.exception(exc)
        st.stop()

    country_df = data["country"]
    global_df = data["global"]
    peaks_df = data["peaks"]
    vaccination_df = data["vaccination"]

    if page == "Overview":
        render_overview(country_df, global_df, peaks_df)
    elif page == "Global Analysis":
        render_global_analysis(global_df)
    elif page == "Country Analysis":
        render_country_analysis(country_df, vaccination_df)
    elif page == "India Analysis":
        render_india_analysis(country_df, global_df, peaks_df, vaccination_df)
    elif page == "Pandemic Trends":
        render_trends(global_df)
    elif page == "Peak Analysis":
        render_peak_analysis(peaks_df, country_df)
    elif page == "Vaccination Analysis":
        render_vaccination(country_df, vaccination_df)
    elif page == "Country Comparison":
        render_comparison(country_df)
    elif page == "Country Rankings":
        render_rankings(country_df)
    elif page == "Data Explorer":
        render_data_explorer(country_df, global_df)
    elif page == "Insights":
        render_insights_page(country_df, global_df, peaks_df)
    else:
        render_about(country_df, global_df)

    st.markdown(
        '<div class="footer">COVID-19 Pandemic Trend Analysis · Reported surveillance data from project CSV files</div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    _init_session()
    if not st.session_state.authenticated:
        render_auth()
        return
    page = render_sidebar()
    render_dashboard(page)


main()
