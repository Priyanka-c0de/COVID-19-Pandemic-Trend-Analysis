# COVID-19 Pandemic Trend Analysis

An authenticated Streamlit web application for exploring reported COVID-19 cases, deaths, pandemic peaks, and vaccination coverage using the datasets already included in this repository.

The application is intended for a college faculty demonstration: it keeps the original analysis files, adds SQLite user accounts, and presents a professional dashboard without fabricating statistics.

## 🚀 Deployment

**Live Demo:** [COVID-19 Pandemic Trend Analysis Dashboard](https://covid-19-pandemic-trend-analysis-qtsmwrvjvdmeebfmgn5mpt.streamlit.app/)

The application is deployed on Streamlit Cloud. You can access the live dashboard using the link above.

## Objectives

- Provide a working, login-protected analytics dashboard.
- Preserve and improve the existing overview, comparison, rankings, trends, peak, vaccination, and data explorer features.
- Load data with stable paths from the project root.
- Show only metrics that can be calculated from the supplied CSV files.
- Document data limitations clearly (no daily country case series, no Indian state data, incomplete vaccination coverage).

## Features

1. User registration with validation
2. User login
3. bcrypt password hashing
4. SQLite user database (`database/app.db`)
5. Session-based access after login
6. Logout
7. Protected dashboard (analytics are hidden until sign-in)
8. Sidebar navigation and signed-in user details
9. Overview KPIs and global trend
10. Global analysis with date filters
11. Country analysis from the location snapshot
12. Dedicated India analysis
13. Pandemic trends with metric selection
14. Peak analysis
15. Vaccination analysis
16. Multi-country comparison
17. Country rankings
18. Data explorer
19. CSV download
20. Dynamic insights generated from the loaded tables
21. Error handling for missing files and empty selections
22. Professional layout and chart styling

## Technology stack

- Python 3
- Streamlit
- Pandas
- Plotly
- SQLite
- bcrypt

No React, Node.js, Docker, cloud databases, or JWT APIs are used.

## Architecture

```
Browser  →  Streamlit UI  →  Auth (session)  →  SQLite (users)
                               ↓
                          Data loader
                               ↓
               CSV files in data/ and notebooks/
                               ↓
                     Pandas + Plotly views
```

`dashboard/app.py` is the single entry point. Unauthenticated visitors only see sign-in and registration. After a successful login, the sidebar exposes the analytics modules.

## Dataset source

The included files are processed extracts originally derived from **Our World in Data (OWID)** COVID-19 data. The notebook `notebooks/01_Data_Collection.ipynb` documents collection from `owid-covid-data.csv`.

This application never downloads live COVID-19 statistics. It only reads the local CSVs listed below.

## Data processing

On load, the application:

- Resolves files from the repository root (independent of the terminal working directory, as long as `app.py` remains in `dashboard/`)
- Checks required columns
- Converts dates and numeric fields
- Drops blank location names and duplicate location rows
- Computes 7-day averages only if those columns are missing from `global_daily.csv`
- Joins the latest non-missing vaccination observation from the five-country time series onto the country snapshot **in memory** (original CSVs are not modified)

Case fatality rate in the snapshot is deaths ÷ cases × 100.

## Files used at runtime

| File | Role |
| --- | --- |
| `data/dashboard_country.csv` | One row per location: totals, rates, peak, optional vaccination |
| `data/global_daily.csv` | Worldwide daily new cases and deaths (2020-01-01 to 2023-10-24 in this copy) |
| `notebooks/country_peaks.csv` | Peak 7-day cases and peak cases per million |
| `notebooks/vaccination_peak_analysis.csv` | Vaccination time series for Brazil, Germany, India, United Kingdom, United States |
| `notebooks/country_summary.csv` | Supporting extract (not required to launch the app) |

## Database design

SQLite file: `database/app.db` (created automatically on first launch).

**users**

| Column | Description |
| --- | --- |
| id | Integer primary key |
| full_name | Display name |
| username | Unique, case-insensitive |
| email | Unique, case-insensitive |
| password_hash | bcrypt hash |
| created_at | UTC timestamp |

**user_activity** (optional audit trail)

| Column | Description |
| --- | --- |
| id | Integer primary key |
| user_id | Foreign key to users |
| action | `register`, `login`, or `logout` |
| created_at | UTC timestamp |

Passwords are never stored in plain text.

## Authentication

- Registration requires full name, username (3–30 letters, numbers, or underscores), email, password (minimum 8 characters), and password confirmation.
- Duplicate usernames and emails are rejected.
- Login checks the hash in SQLite.
- `st.session_state` holds the signed-in user until Sign out is used.
- Analytics pages do not render unless `authenticated` is true.

## Dashboard modules

- **Overview** — KPI cards, global 7-day case trend, map of reported cases, top locations, short insights
- **Global Analysis** — new cases/deaths and 7-day averages with a date range filter
- **Country Analysis** — snapshot metrics for a selected location; vaccination series only if that country is in the five-country file
- **India Analysis** — national India metrics and vaccination series; states are not in the data
- **Pandemic Trends** — selectable global metric and date filter
- **Peak Analysis** — ranking and scatter of peak intensity
- **Vaccination Analysis** — coverage vs peak severity and the five-country time series
- **Country Comparison** — multiple locations, shared metrics
- **Country Rankings** — Top N bar chart and table
- **Data Explorer** — search, filters, sortable table, CSV download
- **Insights** — text generated from the current tables
- **About** — methods, sources, and limitations

## Installation

From the project root:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run instructions

Always start Streamlit from the project root:

```bash
streamlit run dashboard/app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

Create an account on first use, then sign in.

## Project structure

```
COVID-19-Pandemic-Trend-Analysis-master/
├── auth/auth.py
├── database/database.py
├── dashboard/
│   ├── app.py
│   ├── views.py
│   ├── components/
│   └── utils/
├── data/
│   ├── dashboard_country.csv
│   └── global_daily.csv
├── notebooks/
├── requirements.txt
└── README.md
```

## Limitations

- There is **no daily country-level case series** in the supplied files, so country pages do not invent daily case charts.
- **Indian state/district data is not included.**
- Vaccination time series exist for **five countries only**. Many locations have blank vaccination fields in the snapshot; those blanks are not filled in with estimates.
- The country snapshot vaccination columns can be earlier than the five-country time series. Where a later observation exists, the dashboard prefers that later value for display.
- `country_peaks.csv` includes a few territories that are not in `dashboard_country.csv`.
- Late dates in `global_daily.csv` include zeros; "latest new cases" uses the last date with a non-zero case count.
- Reported cases and deaths reflect surveillance systems, not a complete count of all infections.

## Future enhancements

- Add daily country case files if a complete extract becomes available
- Add Indian state-level data from an official source
- Expand vaccination coverage beyond the five-country series
- Add role-based access or password reset if the demo is deployed to a shared server
