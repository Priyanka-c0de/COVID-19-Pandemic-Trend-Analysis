"""Load and validate project datasets using paths relative to the repository root."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"

COUNTRY_NUMERIC = [
    "total_cases",
    "total_deaths",
    "population",
    "cases_per_million",
    "deaths_per_million",
    "case_fatality_rate",
    "peak_7day_cases",
    "peak_cases_per_million",
    "people_vaccinated_per_hundred",
    "people_fully_vaccinated_per_hundred",
    "total_vaccinations_per_hundred",
]

GLOBAL_NUMERIC = [
    "new_cases",
    "new_deaths",
    "new_cases_7day_avg",
    "new_deaths_7day_avg",
]


def _require_file(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(f"Required data file was not found: {path}")
    return path


def _coerce_numeric(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    result = frame.copy()
    for column in columns:
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce")
    return result


def _load_country_dashboard() -> pd.DataFrame:
    path = _require_file(DATA_DIR / "dashboard_country.csv")
    frame = pd.read_csv(path)
    required = ["location", "total_cases", "total_deaths"]
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"dashboard_country.csv is missing columns: {missing}")

    frame = frame.dropna(subset=["location"])
    frame["location"] = frame["location"].astype(str).str.strip()
    frame = frame[frame["location"] != ""]
    frame = frame.drop_duplicates(subset=["location"], keep="first")
    frame = _coerce_numeric(frame, COUNTRY_NUMERIC)

    if "peak_date" in frame.columns:
        frame["peak_date"] = pd.to_datetime(frame["peak_date"], errors="coerce")

    if "case_fatality_rate" not in frame.columns:
        cases = frame["total_cases"].replace(0, pd.NA)
        frame["case_fatality_rate"] = (frame["total_deaths"] / cases) * 100

    return frame.reset_index(drop=True)


def _load_global_daily() -> pd.DataFrame:
    path = _require_file(DATA_DIR / "global_daily.csv")
    frame = pd.read_csv(path)
    if "date" not in frame.columns:
        raise ValueError("global_daily.csv is missing the date column.")

    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame = frame.dropna(subset=["date"])
    frame = frame.drop_duplicates(subset=["date"], keep="first")
    frame = _coerce_numeric(frame, GLOBAL_NUMERIC)
    frame = frame.sort_values("date")

    if "new_cases_7day_avg" not in frame.columns and "new_cases" in frame.columns:
        frame["new_cases_7day_avg"] = frame["new_cases"].rolling(7, min_periods=1).mean()
    if "new_deaths_7day_avg" not in frame.columns and "new_deaths" in frame.columns:
        frame["new_deaths_7day_avg"] = frame["new_deaths"].rolling(7, min_periods=1).mean()

    return frame.reset_index(drop=True)


def _load_peaks() -> pd.DataFrame:
    candidates = [
        DATA_DIR / "country_peaks.csv",
        NOTEBOOK_DIR / "country_peaks.csv",
    ]
    path = next((item for item in candidates if item.exists()), None)
    if path is None:
        return pd.DataFrame()

    frame = pd.read_csv(path)
    if "location" not in frame.columns:
        return pd.DataFrame()

    frame["location"] = frame["location"].astype(str).str.strip()
    frame = frame.drop_duplicates(subset=["location"], keep="first")
    if "peak_date" in frame.columns:
        frame["peak_date"] = pd.to_datetime(frame["peak_date"], errors="coerce")
    for column in frame.columns:
        if column not in {"location", "peak_date"}:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.reset_index(drop=True)


def _load_vaccination_series() -> pd.DataFrame:
    path = NOTEBOOK_DIR / "vaccination_peak_analysis.csv"
    if not path.exists():
        return pd.DataFrame()

    frame = pd.read_csv(path)
    required = ["location", "date"]
    if any(column not in frame.columns for column in required):
        return pd.DataFrame()

    frame["location"] = frame["location"].astype(str).str.strip()
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame = frame.dropna(subset=["location", "date"])
    frame = frame.drop_duplicates(subset=["location", "date"], keep="last")
    for column in [
        "people_vaccinated_per_hundred",
        "people_fully_vaccinated_per_hundred",
        "total_vaccinations_per_hundred",
    ]:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.sort_values(["location", "date"]).reset_index(drop=True)


def _latest_vaccination_snapshot(series: pd.DataFrame) -> pd.DataFrame:
    if series.empty:
        return pd.DataFrame(columns=["location"])

    latest_rows = []
    for location, group in series.groupby("location"):
        row = {"location": location}
        for column in [
            "people_vaccinated_per_hundred",
            "people_fully_vaccinated_per_hundred",
            "total_vaccinations_per_hundred",
        ]:
            if column not in group.columns:
                continue
            observed = group.dropna(subset=[column])
            if observed.empty:
                row[f"latest_{column}"] = pd.NA
                row[f"latest_{column}_date"] = pd.NaT
            else:
                last = observed.iloc[-1]
                row[f"latest_{column}"] = last[column]
                row[f"latest_{column}_date"] = last["date"]
        latest_rows.append(row)
    return pd.DataFrame(latest_rows)


@st.cache_data(show_spinner=False)
def load_all_data() -> dict[str, pd.DataFrame]:
    country_df = _load_country_dashboard()
    global_df = _load_global_daily()
    peaks_df = _load_peaks()
    vaccination_df = _load_vaccination_series()
    latest_vax = _latest_vaccination_snapshot(vaccination_df)

    if not latest_vax.empty:
        country_df = country_df.merge(latest_vax, on="location", how="left")

    return {
        "country": country_df,
        "global": global_df,
        "peaks": peaks_df,
        "vaccination": vaccination_df,
        "data_start": global_df["date"].min() if not global_df.empty else pd.NaT,
        "data_end": global_df["date"].max() if not global_df.empty else pd.NaT,
    }
