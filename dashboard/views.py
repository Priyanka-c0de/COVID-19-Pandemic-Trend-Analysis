"""Dashboard page renderers."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from dashboard.components.charts import (
    bar_chart,
    choropleth_cases,
    dual_axis_global,
    grouped_bar,
    line_chart,
    scatter_chart,
)
from dashboard.components.insights import render_insights
from dashboard.components.kpis import page_header, render_kpi_row
from dashboard.utils.calculations import (
    build_overview_kpis,
    format_date,
    format_number,
    format_percent,
    generate_dynamic_insights,
    get_available_countries,
    get_country_data,
    get_top_countries,
    vaccination_display_value,
)

METRIC_LABELS = {
    "total_cases": "Total cases",
    "total_deaths": "Total deaths",
    "cases_per_million": "Cases per million",
    "deaths_per_million": "Deaths per million",
    "case_fatality_rate": "Case fatality rate (%)",
    "peak_cases_per_million": "Peak cases per million",
    "peak_7day_cases": "Peak 7-day cases",
    "people_fully_vaccinated_per_hundred": "Fully vaccinated (%)",
    "people_vaccinated_per_hundred": "Vaccinated (%)",
    "new_cases": "New cases",
    "new_deaths": "New deaths",
    "new_cases_7day_avg": "7-day average cases",
    "new_deaths_7day_avg": "7-day average deaths",
}


def _label(column: str) -> str:
    return METRIC_LABELS.get(column, column.replace("_", " ").title())


def _safe_metric(value, kind: str = "number") -> str:
    if kind == "percent":
        return format_percent(value)
    if kind == "date":
        return format_date(value)
    return format_number(value)


def _date_filter(global_df: pd.DataFrame, key: str) -> pd.DataFrame:
    min_date = global_df["date"].min().date()
    max_date = global_df["date"].max().date()
    selected = st.slider(
        "Date range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        key=key,
        format="YYYY-MM-DD",
    )
    start, end = selected
    mask = (global_df["date"] >= pd.Timestamp(start)) & (global_df["date"] <= pd.Timestamp(end))
    return global_df.loc[mask].copy()


def render_overview(country_df: pd.DataFrame, global_df: pd.DataFrame, peaks_df: pd.DataFrame) -> None:
    page_header(
        "Overview",
        "Reported COVID-19 cases, deaths, and peak intensity from the project datasets.",
    )
    kpis = build_overview_kpis(country_df, global_df)
    latest_note = (
        f"Last non-zero daily report: {format_date(kpis['latest_date'])}"
        if kpis["latest_date"] is not None
        else "No non-zero daily cases were found"
    )
    render_kpi_row(
        [
            {
                "label": "Reported cases",
                "value": format_number(kpis["total_cases"]),
                "description": "Sum of location totals in the country file",
            },
            {
                "label": "Reported deaths",
                "value": format_number(kpis["total_deaths"]),
                "description": "Sum of location totals in the country file",
            },
            {
                "label": "Locations",
                "value": f"{kpis['locations']:,}",
                "description": "Countries and territories in the snapshot",
            },
            {
                "label": "Latest new cases",
                "value": format_number(kpis["latest_new_cases"]),
                "description": latest_note,
            },
        ]
    )

    st.markdown('<div class="section-title">Global 7-day case trend</div>', unsafe_allow_html=True)
    if global_df.empty or "new_cases_7day_avg" not in global_df.columns:
        st.warning("Global 7-day average cases are not available.")
    else:
        trend = global_df.dropna(subset=["date", "new_cases_7day_avg"])
        st.plotly_chart(
            line_chart(trend, "date", "new_cases_7day_avg", "Global 7-day average of new cases", "New cases"),
            width="stretch",
        )

    left, right = st.columns((1.15, 0.85))
    with left:
        st.markdown('<div class="section-title">Geographic distribution</div>', unsafe_allow_html=True)
        st.plotly_chart(choropleth_cases(country_df), width="stretch")
        st.caption("Unmapped territories are omitted by the chart library; values still appear in tables.")
    with right:
        st.markdown('<div class="section-title">Highest reported cases</div>', unsafe_allow_html=True)
        top = get_top_countries(country_df, "total_cases", 10).sort_values("total_cases")
        st.plotly_chart(
            bar_chart(top, "total_cases", "location", "Top 10 locations by reported cases", orientation="h"),
            width="stretch",
        )

    st.markdown('<div class="section-title">Summary insights</div>', unsafe_allow_html=True)
    render_insights(generate_dynamic_insights(country_df, global_df, peaks_df)[:4])


def render_global_analysis(global_df: pd.DataFrame) -> None:
    page_header(
        "Global analysis",
        "Daily worldwide new cases and deaths from global_daily.csv (1 Jan 2020–24 Oct 2023 in this file).",
    )
    if global_df.empty:
        st.warning("Global daily data is not available.")
        return

    filtered = _date_filter(global_df, "global_dates")
    peak_case_date = (
        format_date(filtered.loc[filtered["new_cases"].idxmax(), "date"])
        if filtered["new_cases"].notna().any()
        else "Not available"
    )
    peak_death_date = (
        format_date(filtered.loc[filtered["new_deaths"].idxmax(), "date"])
        if filtered["new_deaths"].notna().any()
        else "Not available"
    )
    render_kpi_row(
        [
            {
                "label": "Days in range",
                "value": f"{len(filtered):,}",
                "description": f"{format_date(filtered['date'].min())} – {format_date(filtered['date'].max())}",
            },
            {
                "label": "Peak daily cases",
                "value": format_number(filtered["new_cases"].max()),
                "description": peak_case_date,
            },
            {
                "label": "Peak daily deaths",
                "value": format_number(filtered["new_deaths"].max()),
                "description": peak_death_date,
            },
            {
                "label": "Peak 7-day cases",
                "value": format_number(filtered["new_cases_7day_avg"].max()),
                "description": "Highest 7-day average in the selected window",
            },
        ]
    )

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            line_chart(filtered, "date", "new_cases", "New cases over time", "New cases"),
            width="stretch",
        )
    with c2:
        st.plotly_chart(
            line_chart(filtered, "date", "new_deaths", "New deaths over time", "New deaths"),
            width="stretch",
        )
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(
            line_chart(filtered, "date", "new_cases_7day_avg", "7-day average cases", "7-day avg. cases"),
            width="stretch",
        )
    with c4:
        st.plotly_chart(
            line_chart(filtered, "date", "new_deaths_7day_avg", "7-day average deaths", "7-day avg. deaths"),
            width="stretch",
        )
    st.plotly_chart(dual_axis_global(filtered), width="stretch")


def render_country_analysis(country_df: pd.DataFrame, vaccination_df: pd.DataFrame) -> None:
    page_header(
        "Country analysis",
        "Location-level snapshot metrics. Daily case series are not included in the supplied country file.",
    )
    st.markdown(
        '<div class="note-box">This dataset stores one row per location (cumulative totals, rates, peak date, and optional vaccination). '
        "Daily country-level case charts are not generated because those series are not in the project files. "
        "Vaccination time series exist only for India, Brazil, Germany, the United Kingdom, and the United States.</div>",
        unsafe_allow_html=True,
    )
    countries = get_available_countries(country_df)
    selected = st.selectbox("Location", countries, index=countries.index("India") if "India" in countries else 0)
    row = get_country_data(country_df, selected)
    if row is None:
        st.warning("No information is available for this location.")
        return

    render_kpi_row(
        [
            {"label": "Total cases", "value": format_number(row.get("total_cases")), "description": selected},
            {"label": "Total deaths", "value": format_number(row.get("total_deaths")), "description": selected},
            {"label": "Cases per million", "value": format_number(row.get("cases_per_million")), "description": "Population-adjusted"},
            {"label": "Deaths per million", "value": format_number(row.get("deaths_per_million")), "description": "Population-adjusted"},
        ]
    )
    vax = vaccination_display_value(row, "people_fully_vaccinated_per_hundred")
    render_kpi_row(
        [
            {"label": "Case fatality rate", "value": format_percent(row.get("case_fatality_rate")), "description": "Deaths ÷ cases × 100"},
            {"label": "Peak date", "value": format_date(row.get("peak_date")), "description": "Peak of 7-day cases"},
            {"label": "Peak 7-day cases", "value": format_number(row.get("peak_7day_cases")), "description": "Highest 7-day case average"},
            {"label": "Fully vaccinated", "value": format_percent(vax, 1), "description": "Latest series value when available, otherwise snapshot"},
        ]
    )

    details = pd.DataFrame(
        {
            "Metric": [
                "Population",
                "Total cases",
                "Total deaths",
                "Cases per million",
                "Deaths per million",
                "Case fatality rate (%)",
                "Peak date",
                "Peak 7-day cases",
                "Peak cases per million",
                "Vaccinated per 100 (snapshot)",
                "Fully vaccinated per 100 (snapshot)",
                "Fully vaccinated per 100 (latest series)",
            ],
            "Value": [
                _safe_metric(row.get("population")),
                _safe_metric(row.get("total_cases")),
                _safe_metric(row.get("total_deaths")),
                _safe_metric(row.get("cases_per_million")),
                _safe_metric(row.get("deaths_per_million")),
                format_percent(row.get("case_fatality_rate")),
                format_date(row.get("peak_date")),
                _safe_metric(row.get("peak_7day_cases")),
                _safe_metric(row.get("peak_cases_per_million")),
                format_percent(row.get("people_vaccinated_per_hundred"), 1),
                format_percent(row.get("people_fully_vaccinated_per_hundred"), 1),
                format_percent(row.get("latest_people_fully_vaccinated_per_hundred"), 1),
            ],
        }
    )
    st.dataframe(details, width="stretch", hide_index=True)

    if not vaccination_df.empty:
        series = vaccination_df[vaccination_df["location"] == selected].dropna(
            subset=["people_fully_vaccinated_per_hundred"]
        )
        if not series.empty:
            st.markdown('<div class="section-title">Vaccination coverage over time</div>', unsafe_allow_html=True)
            st.plotly_chart(
                line_chart(
                    series,
                    "date",
                    ["people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred"],
                    f"Vaccination coverage — {selected}",
                    "People per 100",
                ),
                width="stretch",
            )


def render_india_analysis(
    country_df: pd.DataFrame,
    global_df: pd.DataFrame,
    peaks_df: pd.DataFrame,
    vaccination_df: pd.DataFrame,
) -> None:
    page_header(
        "India analysis",
        "Country-level India metrics from the supplied files. State or district data is not present.",
    )
    st.markdown(
        '<div class="note-box">This project does not include Indian state-level surveillance files. '
        "The analysis below uses India’s national snapshot, peak record, and (where present) vaccination time series.</div>",
        unsafe_allow_html=True,
    )
    row = get_country_data(country_df, "India")
    if row is None:
        st.error("India is not present in dashboard_country.csv.")
        return

    vax = vaccination_display_value(row, "people_fully_vaccinated_per_hundred")
    render_kpi_row(
        [
            {"label": "Total cases", "value": format_number(row.get("total_cases")), "description": "National snapshot"},
            {"label": "Total deaths", "value": format_number(row.get("total_deaths")), "description": "National snapshot"},
            {"label": "Cases per million", "value": format_number(row.get("cases_per_million")), "description": "Population-adjusted"},
            {"label": "Case fatality rate", "value": format_percent(row.get("case_fatality_rate")), "description": "Deaths ÷ cases × 100"},
        ]
    )
    render_kpi_row(
        [
            {"label": "Deaths per million", "value": format_number(row.get("deaths_per_million")), "description": "Population-adjusted"},
            {"label": "Peak date", "value": format_date(row.get("peak_date")), "description": "Peak of 7-day cases"},
            {"label": "Peak 7-day cases", "value": format_number(row.get("peak_7day_cases")), "description": "Highest 7-day case average"},
            {"label": "Fully vaccinated", "value": format_percent(vax, 1), "description": "Latest available observation"},
        ]
    )

    if not vaccination_df.empty:
        series = vaccination_df[vaccination_df["location"] == "India"].dropna(
            subset=["people_fully_vaccinated_per_hundred"]
        )
        if not series.empty:
            st.markdown('<div class="section-title">India vaccination coverage</div>', unsafe_allow_html=True)
            st.plotly_chart(
                line_chart(
                    series,
                    "date",
                    ["people_vaccinated_per_hundred", "people_fully_vaccinated_per_hundred"],
                    "India — people vaccinated per 100",
                    "People per 100",
                ),
                width="stretch",
            )

    peak_row = None
    if not peaks_df.empty:
        match = peaks_df[peaks_df["location"] == "India"]
        if not match.empty:
            peak_row = match.iloc[0]
    if peak_row is not None:
        st.markdown('<div class="section-title">Peak record</div>', unsafe_allow_html=True)
        st.write(
            f"India’s recorded peak of 7-day cases is {format_number(peak_row.get('peak_7day_cases'))} "
            f"on {format_date(peak_row.get('peak_date'))} "
            f"({format_number(peak_row.get('peak_cases_per_million'))} cases per million)."
        )

    if not global_df.empty:
        global_peak = global_df.dropna(subset=["new_cases_7day_avg"]).sort_values(
            "new_cases_7day_avg", ascending=False
        ).iloc[0]
        st.caption(
            f"For context, the global 7-day case average peaked at "
            f"{format_number(global_peak['new_cases_7day_avg'])} on {format_date(global_peak['date'])}."
        )


def render_trends(global_df: pd.DataFrame) -> None:
    page_header(
        "Pandemic trends",
        "Interactive global time series with metric selection, date filtering, zoom, and hover details.",
    )
    if global_df.empty:
        st.warning("No global trend data is available.")
        return

    numeric_columns = [
        column
        for column in global_df.columns
        if column != "date" and pd.api.types.is_numeric_dtype(global_df[column])
    ]
    if not numeric_columns:
        st.warning("No numeric trend columns were found.")
        return

    selected_metric = st.selectbox(
        "Metric",
        numeric_columns,
        format_func=_label,
        index=numeric_columns.index("new_cases_7day_avg") if "new_cases_7day_avg" in numeric_columns else 0,
    )
    filtered = _date_filter(global_df, "trend_dates")
    trend = filtered.dropna(subset=["date", selected_metric])
    fig = line_chart(trend, "date", selected_metric, _label(selected_metric), _label(selected_metric))
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, width="stretch")
    st.caption("Use the Plotly toolbar to zoom, pan, and download the chart.")


def render_peak_analysis(peaks_df: pd.DataFrame, country_df: pd.DataFrame) -> None:
    page_header(
        "Peak analysis",
        "Highest 7-day case intensity by location, using country_peaks.csv when available.",
    )
    source = peaks_df if not peaks_df.empty else country_df
    if source.empty or "peak_cases_per_million" not in source.columns:
        st.warning("Peak analysis data is not available.")
        return

    top_n = st.slider("Number of locations", 5, 25, 15, key="peak_n")
    top = (
        source.dropna(subset=["peak_cases_per_million"])
        .sort_values("peak_cases_per_million", ascending=False)
        .head(top_n)
        .sort_values("peak_cases_per_million")
    )
    st.plotly_chart(
        bar_chart(top, "peak_cases_per_million", "location", "Peak 7-day cases per million", orientation="h"),
        width="stretch",
    )

    if "peak_date" in source.columns:
        dated = source.dropna(subset=["peak_date", "peak_7day_cases"]) if "peak_7day_cases" in source.columns else source.dropna(subset=["peak_date"])
        if not dated.empty and "peak_7day_cases" in dated.columns:
            st.markdown('<div class="section-title">Peak timing versus intensity</div>', unsafe_allow_html=True)
            scatter = dated.copy()
            scatter["peak_date_str"] = scatter["peak_date"].dt.strftime("%Y-%m-%d")
            st.plotly_chart(
                scatter_chart(
                    scatter,
                    "peak_date",
                    "peak_cases_per_million",
                    "location",
                    "peak_7day_cases",
                    "When peaks occurred (size = peak 7-day cases)",
                ),
                width="stretch",
            )

    display_cols = [c for c in ["location", "peak_date", "peak_7day_cases", "peak_cases_per_million"] if c in source.columns]
    ranking = source[display_cols].sort_values("peak_cases_per_million", ascending=False)
    st.markdown('<div class="section-title">Peak records</div>', unsafe_allow_html=True)
    st.dataframe(ranking, width="stretch", hide_index=True)


def render_vaccination(country_df: pd.DataFrame, vaccination_df: pd.DataFrame) -> None:
    page_header(
        "Vaccination analysis",
        "Coverage values from the country snapshot, enriched with later observations for five countries that have a time series.",
    )
    work = country_df.copy()
    if "latest_people_fully_vaccinated_per_hundred" in work.columns:
        work["display_full_vax"] = work["latest_people_fully_vaccinated_per_hundred"].combine_first(
            work.get("people_fully_vaccinated_per_hundred")
        )
    else:
        work["display_full_vax"] = work.get("people_fully_vaccinated_per_hundred")

    scatter_df = work.dropna(subset=["display_full_vax", "peak_cases_per_million"])
    if scatter_df.empty:
        st.warning("Vaccination and peak columns are not jointly available.")
    else:
        st.plotly_chart(
            scatter_chart(
                scatter_df,
                "display_full_vax",
                "peak_cases_per_million",
                "location",
                "population",
                "Full vaccination coverage versus peak cases per million",
            ),
            width="stretch",
        )
        st.caption(
            f"Scatter includes {len(scatter_df):,} locations with both a vaccination value and a peak intensity value. "
            "Many locations have missing vaccination fields and are excluded."
        )

    ranked = work.dropna(subset=["display_full_vax"]).sort_values("display_full_vax", ascending=False).head(15)
    if not ranked.empty:
        st.markdown('<div class="section-title">Highest observed full vaccination coverage</div>', unsafe_allow_html=True)
        st.plotly_chart(
            bar_chart(
                ranked.sort_values("display_full_vax"),
                "display_full_vax",
                "location",
                "Fully vaccinated people per 100",
                orientation="h",
            ),
            width="stretch",
        )

    if not vaccination_df.empty:
        st.markdown('<div class="section-title">Time series for selected countries</div>', unsafe_allow_html=True)
        series = vaccination_df.dropna(subset=["people_fully_vaccinated_per_hundred"])
        st.plotly_chart(
            line_chart(
                series,
                "date",
                "people_fully_vaccinated_per_hundred",
                "Fully vaccinated people per 100",
                "People per 100",
                color="location",
            ),
            width="stretch",
        )


def render_comparison(country_df: pd.DataFrame) -> None:
    page_header("Country comparison", "Compare two or more locations on metrics present in the country snapshot.")
    countries = get_available_countries(country_df)
    defaults = [name for name in ["India", "United States", "Brazil"] if name in countries][:3]
    selected = st.multiselect("Locations", countries, default=defaults)
    if len(selected) < 2:
        st.info("Select at least two locations.")
        return

    comparison = country_df[country_df["location"].isin(selected)].copy()
    if "latest_people_fully_vaccinated_per_hundred" in comparison.columns:
        comparison["vaccination_coverage"] = comparison["latest_people_fully_vaccinated_per_hundred"].combine_first(
            comparison.get("people_fully_vaccinated_per_hundred")
        )
    else:
        comparison["vaccination_coverage"] = comparison.get("people_fully_vaccinated_per_hundred")

    metrics = [
        "total_cases",
        "total_deaths",
        "cases_per_million",
        "deaths_per_million",
        "case_fatality_rate",
        "peak_cases_per_million",
        "vaccination_coverage",
    ]
    available = [metric for metric in metrics if metric in comparison.columns]
    chosen = st.selectbox("Chart metric", available, format_func=_label)
    st.plotly_chart(grouped_bar(comparison, "location", chosen, _label(chosen)), width="stretch")

    table = comparison[["location"] + available].rename(columns=_label)
    st.dataframe(table, width="stretch", hide_index=True)


def render_rankings(country_df: pd.DataFrame) -> None:
    page_header("Country rankings", "Rank locations by a selected metric from the country snapshot.")
    metric_options = [
        "total_cases",
        "total_deaths",
        "cases_per_million",
        "deaths_per_million",
        "case_fatality_rate",
        "peak_cases_per_million",
    ]
    available = [metric for metric in metric_options if metric in country_df.columns]
    top_n = st.slider("Number of locations", 5, 30, 10, key="rank_n")
    metric = st.selectbox("Rank by", available, format_func=_label)
    ranking = (
        country_df.dropna(subset=[metric])
        .sort_values(metric, ascending=False)
        .head(top_n)
    )
    st.plotly_chart(
        bar_chart(ranking.sort_values(metric), metric, "location", _label(metric), orientation="h"),
        width="stretch",
    )
    display = ranking[["location", metric] + [c for c in ["total_cases", "total_deaths", "population"] if c != metric and c in ranking.columns]]
    st.dataframe(display.reset_index(drop=True), width="stretch", hide_index=True)


def render_data_explorer(country_df: pd.DataFrame, global_df: pd.DataFrame) -> None:
    page_header("Data explorer", "Search, filter, sort, and download the loaded tables.")
    dataset = st.radio("Dataset", ["Country snapshot", "Global daily"], horizontal=True)
    if dataset == "Country snapshot":
        countries = ["All"] + get_available_countries(country_df)
        selected_country = st.selectbox("Location filter", countries)
        search = st.text_input("Search location name")
        display_df = country_df.copy()
        if selected_country != "All":
            display_df = display_df[display_df["location"] == selected_country]
        if search:
            display_df = display_df[display_df["location"].astype(str).str.contains(search, case=False, na=False)]
        filename = "covid19_country_snapshot.csv"
    else:
        display_df = _date_filter(global_df, "explorer_dates")
        filename = "covid19_global_daily.csv"

    st.write(f"Showing {len(display_df):,} rows")
    st.dataframe(display_df, width="stretch", hide_index=True)
    st.download_button(
        "Download CSV",
        display_df.to_csv(index=False).encode("utf-8"),
        filename,
        "text/csv",
    )


def render_insights_page(country_df: pd.DataFrame, global_df: pd.DataFrame, peaks_df: pd.DataFrame) -> None:
    page_header(
        "Insights",
        "Statements below are generated from the loaded tables. They are not hard-coded statistics.",
    )
    render_insights(generate_dynamic_insights(country_df, global_df, peaks_df))


def render_about(country_df: pd.DataFrame, global_df: pd.DataFrame) -> None:
    page_header(
        "About",
        "COVID-19 Pandemic Trend Analysis — an authenticated analytics application for academic demonstration.",
    )
    date_range = "not available"
    if not global_df.empty:
        date_range = f"{format_date(global_df['date'].min())} to {format_date(global_df['date'].max())}"
    st.markdown(
        f"""
        ### Purpose
        Explore reported COVID-19 cases, deaths, peak intensity, and vaccination coverage using the datasets
        already included in this repository.

        ### Dataset source
        Processed extracts originally derived from **Our World in Data (OWID)** COVID-19 data.
        This application reads only the local CSV files shipped with the project.

        ### What is in the files
        - **dashboard_country.csv**: {len(country_df):,} location snapshots (cumulative cases, deaths, rates, peaks, partial vaccination).
        - **global_daily.csv**: worldwide daily new cases and deaths, {date_range}.
        - **country_peaks.csv**: peak 7-day case intensity by location.
        - **vaccination_peak_analysis.csv**: vaccination time series for five countries only.

        ### Authentication
        User accounts are stored in a local SQLite database. Passwords are hashed with bcrypt and are never stored in plain text.

        ### Interpretation
        Reporting practices differed by country and over time. Figures are surveillance totals from the supplied files,
        not a complete measure of all infections or deaths. Missing vaccination values are shown as unavailable rather than estimated.
        """
    )
