"""HTML KPI cards."""

from __future__ import annotations

import streamlit as st


def render_kpi_row(cards: list[dict[str, str]]) -> None:
    """Render KPI cards in a responsive Streamlit row."""

    if not cards:
        return

    columns = st.columns(
        len(cards),
        gap="medium",
    )

    for column, card in zip(columns, cards):
        with column:
            label = card.get("label", "")
            value = card.get("value", "—")
            description = card.get("description", "")

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-description">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def page_header(title: str, subtitle: str) -> None:
    """Render a consistent dashboard page header."""

    st.markdown(
        f"""
        <div class="main-title">{title}</div>
        <div class="subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )