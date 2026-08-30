"""SQLite helpers for user accounts and simple activity logging."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "app.db"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def get_connection() -> sqlite3.Connection:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    """Create tables if they do not already exist."""
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS user_activity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        connection.commit()


def create_user(full_name: str, username: str, email: str, password_hash: str) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO users (full_name, username, email, password_hash, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (full_name, username, email, password_hash, utc_now()),
        )
        connection.commit()
        return int(cursor.lastrowid)


def get_user_by_username(username: str) -> sqlite3.Row | None:
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE username = ? COLLATE NOCASE",
            (username,),
        ).fetchone()


def get_user_by_email(email: str) -> sqlite3.Row | None:
    with get_connection() as connection:
        return connection.execute(
            "SELECT * FROM users WHERE email = ? COLLATE NOCASE",
            (email,),
        ).fetchone()


def username_exists(username: str) -> bool:
    return get_user_by_username(username) is not None


def email_exists(email: str) -> bool:
    return get_user_by_email(email) is not None


def log_activity(user_id: int | None, action: str) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO user_activity (user_id, action, created_at)
            VALUES (?, ?, ?)
            """,
            (user_id, action, utc_now()),
        )
        connection.commit()
