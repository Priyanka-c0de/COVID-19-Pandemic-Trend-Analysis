"""Registration, login, and password hashing."""

from __future__ import annotations

import re

import bcrypt

from database.database import (
    create_user,
    email_exists,
    get_user_by_username,
    log_activity,
    username_exists,
)

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_]{3,30}$")
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,79}$")


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )
    except ValueError:
        return False


def validate_registration(
    full_name: str,
    username: str,
    email: str,
    password: str,
    confirm_password: str,
) -> list[str]:
    errors: list[str] = []
    full_name = full_name.strip()
    username = username.strip()
    email = email.strip()

    if not NAME_PATTERN.match(full_name):
        errors.append("Enter a valid full name using letters and spaces.")

    if not USERNAME_PATTERN.match(username):
        errors.append(
            "Username must be 3–30 characters and may contain only letters, numbers, and underscores."
        )

    if not EMAIL_PATTERN.match(email):
        errors.append("Enter a valid email address.")

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if password != confirm_password:
        errors.append("Password confirmation does not match.")

    if username and username_exists(username):
        errors.append("That username is already registered.")

    if email and email_exists(email):
        errors.append("That email address is already registered.")

    return errors


def register_user(
    full_name: str,
    username: str,
    email: str,
    password: str,
    confirm_password: str,
) -> tuple[bool, str]:
    errors = validate_registration(
        full_name, username, email, password, confirm_password
    )
    if errors:
        return False, errors[0]

    user_id = create_user(
        full_name=full_name.strip(),
        username=username.strip(),
        email=email.strip().lower(),
        password_hash=hash_password(password),
    )
    log_activity(user_id, "register")
    return True, "Account created successfully. You can now sign in."


def authenticate_user(username: str, password: str) -> tuple[bool, str, dict | None]:
    if not username.strip() or not password:
        return False, "Enter both username and password.", None

    user = get_user_by_username(username.strip())
    if user is None or not verify_password(password, user["password_hash"]):
        return False, "Invalid username or password.", None

    log_activity(user["id"], "login")
    profile = {
        "id": user["id"],
        "full_name": user["full_name"],
        "username": user["username"],
        "email": user["email"],
        "created_at": user["created_at"],
    }
    return True, "Signed in successfully.", profile
