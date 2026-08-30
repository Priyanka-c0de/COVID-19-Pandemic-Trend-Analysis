"""Render insight cards from dynamically computed text."""

from __future__ import annotations

import streamlit as st


def render_insights(insights: list[dict[str, str]]) -> None:
    if not insights:
        st.info("Insights cannot be generated from the currently loaded data.")
        return

    for item in insights:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">{item["title"]}</div>
                <div class="insight-text">{item["text"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
