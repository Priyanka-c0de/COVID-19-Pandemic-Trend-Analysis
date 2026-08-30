"""KPI helpers and dynamic insights derived only from loaded datasets."""

from __future__ import annotations

import pandas as pd


def format_number(value, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "Not available"
    number = float(value)
    abs_number = abs(number)
    if abs_number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.{digits}f}B"
    if abs_number >= 1_000_000:
        return f"{number / 1_000_000:.{digits}f}M"
    if abs_number >= 1_000:
        return f"{number / 1_000:.{digits}f}K"
    if abs_number >= 100:
        return f"{number:,.0f}"
    return f"{number:,.{digits}f}"


def format_percent(value, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "Not available"
    return f"{float(value):.{digits}f}%"


def format_date(value) -> str:
    if value is None or pd.isna(value):
        return "Not available"
    return pd.to_datetime(value).strftime("%d %b %Y")


def calculate_case_fatality_rate(cases, deaths) -> float:
    if cases is None or pd.isna(cases) or cases == 0:
        return 0.0
    if deaths is None or pd.isna(deaths):
        return 0.0
    return (float(deaths) / float(cases)) * 100


def get_available_countries(df: pd.DataFrame) -> list[str]:
    if "location" not in df.columns:
        return []
    return sorted(df["location"].dropna().unique().tolist())


def get_country_data(df: pd.DataFrame, country: str) -> pd.Series | None:
    result = df[df["location"] == country]
    if result.empty:
        return None
    return result.iloc[0]


def get_top_countries(df: pd.DataFrame, metric: str, top_n: int = 10) -> pd.DataFrame:
    if metric not in df.columns or "location" not in df.columns:
        return pd.DataFrame()
    return (
        df[["location", metric]]
        .dropna()
        .sort_values(metric, ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )


def vaccination_display_value(row: pd.Series, snapshot_column: str) -> float | None:
    latest_column = f"latest_{snapshot_column}"
    if latest_column in row.index and pd.notna(row.get(latest_column)):
        return float(row[latest_column])
    value = row.get(snapshot_column)
    if pd.isna(value):
        return None
    return float(value)


def build_overview_kpis(country_df: pd.DataFrame, global_df: pd.DataFrame) -> dict:
    latest_new_cases = None
    latest_new_deaths = None
    latest_date = None
    if not global_df.empty and "new_cases" in global_df.columns:
        observed = global_df.dropna(subset=["new_cases"])
        observed = observed[observed["new_cases"] > 0]
        if not observed.empty:
            last = observed.iloc[-1]
            latest_new_cases = last["new_cases"]
            latest_date = last["date"]
            if "new_deaths" in last.index:
                latest_new_deaths = last["new_deaths"]

    highest_cases = country_df.dropna(subset=["total_cases"]).sort_values(
        "total_cases", ascending=False
    )
    highest_deaths = country_df.dropna(subset=["total_deaths"]).sort_values(
        "total_deaths", ascending=False
    )

    return {
        "locations": int(country_df["location"].nunique()),
        "total_cases": float(country_df["total_cases"].sum(skipna=True)),
        "total_deaths": float(country_df["total_deaths"].sum(skipna=True)),
        "latest_new_cases": latest_new_cases,
        "latest_new_deaths": latest_new_deaths,
        "latest_date": latest_date,
        "highest_cases_location": (
            highest_cases.iloc[0]["location"] if not highest_cases.empty else None
        ),
        "highest_deaths_location": (
            highest_deaths.iloc[0]["location"] if not highest_deaths.empty else None
        ),
    }


def generate_dynamic_insights(
    country_df: pd.DataFrame,
    global_df: pd.DataFrame,
    peaks_df: pd.DataFrame,
) -> list[dict[str, str]]:
    insights: list[dict[str, str]] = []

    if country_df.empty:
        return [
            {
                "title": "No country records",
                "text": "The country dataset could not be loaded, so insights cannot be generated.",
            }
        ]

    kpis = build_overview_kpis(country_df, global_df)
    insights.append(
        {
            "title": "Surveillance coverage",
            "text": (
                f"The country dataset covers {kpis['locations']:,} locations with a combined "
                f"{format_number(kpis['total_cases'])} reported cases and "
                f"{format_number(kpis['total_deaths'])} reported deaths."
            ),
        }
    )

    if kpis["highest_cases_location"]:
        row = get_country_data(country_df, kpis["highest_cases_location"])
        insights.append(
            {
                "title": "Highest reported cases",
                "text": (
                    f"{kpis['highest_cases_location']} has the highest reported case count "
                    f"({format_number(row['total_cases'])})."
                ),
            }
        )

    populated = country_df.dropna(subset=["case_fatality_rate", "population"])
    populated = populated[populated["population"] >= 1_000_000]
    if not populated.empty:
        severe = populated.sort_values("case_fatality_rate", ascending=False).iloc[0]
        insights.append(
            {
                "title": "Highest case fatality among large populations",
                "text": (
                    f"Among locations with at least 1 million people, {severe['location']} "
                    f"has the highest case fatality rate at {format_percent(severe['case_fatality_rate'])}."
                ),
            }
        )

    peak_source = peaks_df if not peaks_df.empty else country_df
    if "peak_cases_per_million" in peak_source.columns:
        peak_rows = peak_source.dropna(subset=["peak_cases_per_million"])
        if not peak_rows.empty:
            peak = peak_rows.sort_values("peak_cases_per_million", ascending=False).iloc[0]
            peak_date = format_date(peak["peak_date"]) if "peak_date" in peak.index else "an unavailable date"
            insights.append(
                {
                    "title": "Highest recorded peak intensity",
                    "text": (
                        f"{peak['location']} recorded the highest peak 7-day cases per million "
                        f"({format_number(peak['peak_cases_per_million'], 0)}) around {peak_date}."
                    ),
                }
            )

    if not global_df.empty and "new_cases_7day_avg" in global_df.columns:
        global_peaks = global_df.dropna(subset=["new_cases_7day_avg"])
        if not global_peaks.empty:
            global_peak = global_peaks.sort_values("new_cases_7day_avg", ascending=False).iloc[0]
            insights.append(
                {
                    "title": "Global incidence peak",
                    "text": (
                        f"The highest global 7-day average of new cases in this file is "
                        f"{format_number(global_peak['new_cases_7day_avg'])} on "
                        f"{format_date(global_peak['date'])}."
                    ),
                }
            )

    india = get_country_data(country_df, "India")
    if india is not None:
        vax = vaccination_display_value(india, "people_fully_vaccinated_per_hundred")
        vax_text = (
            f" Latest observed full vaccination coverage is {format_percent(vax, 1)}."
            if vax is not None
            else " Full vaccination coverage is not available for India in the snapshot file."
        )
        insights.append(
            {
                "title": "India in this dataset",
                "text": (
                    f"India reports {format_number(india['total_cases'])} cases and "
                    f"{format_number(india['total_deaths'])} deaths, with a case fatality rate of "
                    f"{format_percent(india['case_fatality_rate'])}. Peak 7-day cases occurred around "
                    f"{format_date(india.get('peak_date'))}.{vax_text}"
                ),
            }
        )

    vax_col = "people_fully_vaccinated_per_hundred"
    latest_col = f"latest_{vax_col}"
    vax_frame = country_df.copy()
    if latest_col in vax_frame.columns:
        vax_frame["_vax"] = vax_frame[latest_col].combine_first(vax_frame.get(vax_col))
    else:
        vax_frame["_vax"] = vax_frame.get(vax_col)
    vax_frame = vax_frame.dropna(subset=["_vax", "peak_cases_per_million"])
    if len(vax_frame) >= 8:
        highest_vax = vax_frame.sort_values("_vax", ascending=False).iloc[0]
        insights.append(
            {
                "title": "Vaccination coverage in available records",
                "text": (
                    f"Among locations with vaccination values, {highest_vax['location']} has the "
                    f"highest observed full vaccination coverage ({format_percent(highest_vax['_vax'], 1)}). "
                    "Coverage is missing for many locations, so this is not a complete global ranking."
                ),
            }
        )

    return insights
