"""HTML KPI cards."""

from __future__ import annotations

import streamlit as st


def render_kpi_row(cards: list[dict[str, str]]) -> None:
    columns = st.columns(len(cards))
    for column, card in zip(columns, cards):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{card["label"]}</div>
                    <div class="metric-value">{card["value"]}</div>
                    <div class="metric-description">{card.get("description", "")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def page_header(title: str, subtitle: str) -> None:
    st.markdown(f'<div class="main-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)
