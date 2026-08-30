"""Headless checks for authentication, data loading, and insight generation."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from auth.auth import authenticate_user, hash_password, register_user, verify_password
from dashboard.utils.calculations import generate_dynamic_insights
from dashboard.utils.data_loader import (
    _load_country_dashboard,
    _load_global_daily,
    _load_peaks,
    _load_vaccination_series,
)
from database.database import DATABASE_PATH, get_user_by_username, init_db


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")


def main() -> None:
    init_db()
    expect(DATABASE_PATH.parent.exists(), "database directory exists")

    password = "TestPass123!"
    hashed = hash_password(password)
    expect(hashed != password, "password hash is not plain text")
    expect(hashed.startswith("$2"), "hash looks like bcrypt")
    expect(verify_password(password, hashed), "correct password verifies")
    expect(not verify_password("wrong-password", hashed), "wrong password is rejected")

    suffix = "demo"
    username = f"faculty_{suffix}"
    email = f"faculty_{suffix}@college.edu"
    existing = get_user_by_username(username)
    if existing is None:
        ok, message = register_user("Faculty Demo", username, email, password, password)
        expect(ok, f"registration succeeds ({message})")
    else:
        print("OK: demo user already present")

    ok, message = register_user("Faculty Demo", username, email, password, password)
    expect(not ok, f"duplicate registration rejected ({message})")

    ok, message, profile = authenticate_user(username, password)
    expect(ok and profile is not None, f"login succeeds ({message})")
    ok, message, profile = authenticate_user(username, "bad-password")
    expect(not ok and profile is None, f"wrong password login rejected ({message})")

    with sqlite3.connect(DATABASE_PATH) as connection:
        stored = connection.execute(
            "SELECT password_hash FROM users WHERE username = ?",
            (username,),
        ).fetchone()[0]
    expect(stored != password, "database does not store the plain password")
    expect(verify_password(password, stored), "stored hash matches the demo password")

    country = _load_country_dashboard()
    global_df = _load_global_daily()
    peaks = _load_peaks()
    vax = _load_vaccination_series()
    expect(len(country) == 232, f"country snapshot row count is {len(country)}")
    expect("India" in set(country["location"]), "India is in the country snapshot")
    expect(len(global_df) > 1000, "global daily file loaded")
    expect(not peaks.empty, "peak file loaded")
    expect(set(vax["location"]) == {"Brazil", "Germany", "India", "United Kingdom", "United States"}, "vaccination series countries")

    insights = generate_dynamic_insights(country, global_df, peaks)
    expect(len(insights) >= 3, "dynamic insights were generated")
    print("\nAll verification checks passed.")


if __name__ == "__main__":
    main()
