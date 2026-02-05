"""Validation utilities for the application."""
from typing import Optional
import re


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> bool:
    """Validate password strength."""
    # Password should be at least 8 characters with at least one uppercase,
    # one lowercase, one digit, and one special character
    if len(password) < 8:
        return False

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    return has_upper and has_lower and has_digit and has_special


def validate_username(username: str) -> bool:
    """Validate username format."""
    # Username should be 3-20 characters, alphanumeric and underscores only
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))