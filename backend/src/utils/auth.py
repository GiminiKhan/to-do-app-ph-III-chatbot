"""Authentication utilities for the application."""
from fastapi import HTTPException, status
from typing import Optional
import bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    # Ensure both are strings
    if not isinstance(plain_password, str):
        plain_password = str(plain_password)

    if not isinstance(hashed_password, str):
        hashed_password = str(hashed_password)

    # Ensure plain password is within bcrypt's 72-byte limit
    plain_password_bytes = plain_password.encode('utf-8')
    if len(plain_password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string
        plain_password = plain_password_bytes[:72].decode('utf-8', errors='ignore')

    try:
        # Encode both passwords to bytes for bcrypt
        plain_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password

        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except ValueError as e:
        # Handle bcrypt value errors (like the 72-byte limit)
        if "password cannot be longer than 72 bytes" in str(e):
            return False
        raise


def get_password_hash(password: str) -> str:
    """Hash a password."""
    # Ensure password is a string
    if not isinstance(password, str):
        password = str(password)

    # Ensure password is within bcrypt's 72-byte limit
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes and decode back to string
        password = password_bytes[:72].decode('utf-8', errors='ignore')

    # Hash the password using bcrypt directly
    password_bytes = password.encode('utf-8')

    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Return as string
    return hashed.decode('utf-8')