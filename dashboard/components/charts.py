"""Reusable Plotly chart helpers with a consistent professional theme."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


COLOR_PRIMARY = "#0f4c5c"
COLOR_ACCENT = "#e36414"
COLOR_LINE = "#1d4e89"
COLOR_DEATHS = "#9a031e"
COLOR_TEAL = "#0d9488"

SEQUENTIAL = [
    "#0b1f33",
    "#0f4c5c",
    "#1d4e89",
    "#0d9488",
    "#e36414",
]


LAYOUT = dict(
    template="plotly_white",

    font=dict(
        family="Source Sans 3, Segoe UI, Helvetica, Arial, sans-serif",
        color="#1a2332",
        size=13,
    ),

    margin=dict(
        l=55,
        r=35,
        t=65,
        b=50,
    ),

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        x=0,
        font=dict(
            color="#475569",
            size=12,
        ),
    ),

    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#dbe4ea",
        font_size=12,
        font_family="Source Sans 3, Segoe UI, Helvetica, Arial, sans-serif",
        font_color="#0b1f33",
    ),

    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",

    title_font=dict(
        family="Source Sans 3, Segoe UI, Helvetica, Arial, sans-serif",
        color="#0b1f33",
        size=17,
    ),

    xaxis=dict(
        title_font=dict(
            color="#334155",
            size=13,
        ),
        tickfont=dict(
            color="#475569",
            size=11,
        ),
        linecolor="#cbd5e1",
        linewidth=1,
    ),

    yaxis=dict(
        title_font=dict(
            color="#334155",
            size=13,
        ),
        tickfont=dict(
            color="#475569",
            size=11,
        ),
        linecolor="#cbd5e1",
        linewidth=1,
    ),
)


def apply_layout(
    fig,
    height: int = 440,
    y_title: str = "",
    x_title: str = "",
):
    """Apply the shared professional chart layout."""

    fig.update_layout(
        **LAYOUT,
        height=height,
    )

    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
    )

    fig.update_yaxes(
        gridcolor="#edf1f4",
        gridwidth=1,
        zeroline=False,
    )

    return fig


def line_chart(
    df: pd.DataFrame,
    x: str,
    y,
    title: str,
    y_title: str = "",
    color=None,
):
    """Create a consistent line chart."""

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        color_discrete_sequence=SEQUENTIAL,
    )

    fig.update_traces(
        line=dict(width=2.2),
        hovertemplate="%{x|%d %b %Y}<br>%{y:,.1f}<extra></extra>",
    )

    return apply_layout(
        fig,
        y_title=y_title,
        x_title="Date",
    )


def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    orientation: str = "v",
):
    """Create a consistent bar chart."""

    if orientation == "h":
        fig = px.bar(
            df,
            x=x,
            y=y,
            orientation="h",
            title=title,
            color_discrete_sequence=[COLOR_PRIMARY],
            text_auto=".2s",
        )

        fig.update_traces(
            hovertemplate="%{y}<br>%{x:,.2f}<extra></extra>"
        )

        return apply_layout(
            fig,
            height=max(420, 28 * len(df) + 120),
            x_title=x.replace("_", " ").title(),
            y_title="",
        )

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=[COLOR_PRIMARY],
        text_auto=".2s",
    )

    fig.update_traces(
        hovertemplate="%{x}<br>%{y:,.2f}<extra></extra>"
    )

    return apply_layout(
        fig,
        y_title=y.replace("_", " ").title(),
        x_title="",
    )


def grouped_bar(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
):
    """Create a grouped categorical bar chart."""

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        color=x,
        color_discrete_sequence=SEQUENTIAL,
        text_auto=".2s",
    )

    fig.update_layout(
        showlegend=False,
    )

    return apply_layout(
        fig,
        y_title=y.replace("_", " ").title(),
    )


def scatter_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    hover: str,
    size: str | None,
    title: str,
):
    """Create a professional scatter chart."""

    fig = px.scatter(
        df,
        x=x,
        y=y,
        hover_name=hover,
        size=size if size and size in df.columns else None,
        title=title,
        color_discrete_sequence=[COLOR_TEAL],
    )

    fig.update_traces(
        marker=dict(
            opacity=0.75,
            line=dict(
                width=0.5,
                color="white",
            ),
        )
    )

    return apply_layout(
        fig,
        height=520,
        x_title=x.replace("_", " ").title(),
        y_title=y.replace("_", " ").title(),
    )


def choropleth_cases(
    df: pd.DataFrame,
):
    """Create the global reported-cases choropleth."""

    plot_df = df.dropna(
        subset=["location", "total_cases"]
    ).copy()

    fig = px.choropleth(
        plot_df,
        locations="location",
        locationmode="country names",
        color="total_cases",
        hover_name="location",
        hover_data={
            "total_cases": ":,.0f",
            "total_deaths": ":,.0f",
            "location": False,
        },
        color_continuous_scale=[
            "#e8f1f2",
            "#0d9488",
            "#0f4c5c",
            "#0b1f33",
        ],
        title="Reported cases by country or territory",
    )

    fig.update_layout(
        **LAYOUT,
        height=520,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#cbd5e1",
            bgcolor="#f8fafb",
        ),
        coloraxis_colorbar=dict(
            title="Cases",
        ),
    )

    return fig


def dual_axis_global(
    df: pd.DataFrame,
):
    """Create global 7-day case and death averages."""

    fig = go.Figure()

    # 7-day average cases
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["new_cases_7day_avg"],
            name="7-day avg. cases",
            line=dict(
                color=COLOR_LINE,
                width=2.2,
            ),
        )
    )

    # 7-day average deaths
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["new_deaths_7day_avg"],
            name="7-day avg. deaths",
            yaxis="y2",
            line=dict(
                color=COLOR_DEATHS,
                width=2.2,
            ),
        )
    )

    # Remove the original yaxis from the shared layout
    # before defining the two-axis configuration.
    dual_layout = {
        key: value
        for key, value in LAYOUT.items()
        if key != "yaxis"
    }

    fig.update_layout(
        **dual_layout,
        height=460,
        title="Global 7-day averages: cases and deaths",

        yaxis=dict(
            title="New cases (7-day avg.)",
            gridcolor="#edf1f4",
            gridwidth=1,
            title_font=dict(
                color="#334155",
                size=13,
            ),
            tickfont=dict(
                color="#475569",
                size=11,
            ),
            linecolor="#cbd5e1",
        ),

        yaxis2=dict(
            title="New deaths (7-day avg.)",
            overlaying="y",
            side="right",
            title_font=dict(
                color="#334155",
                size=13,
            ),
            tickfont=dict(
                color="#475569",
                size=11,
            ),
            linecolor="#cbd5e1",
        ),

        xaxis_title="Date",
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
    )

    fig.update_yaxes(
        zeroline=False,
    )

    return fig