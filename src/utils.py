"""
utils.py — Shared helper utilities.

Provides:
  - current_timestamp(): ISO 8601 datetime string
  - today_str():         today's date as YYYY-MM-DD
  - unique_id():         short unique ID for each log entry
  - parse_json_safely(): parse a JSON string and return None on failure
"""

import datetime
import json
import uuid


def current_timestamp() -> str:
    """Return the current date and time as an ISO 8601 string."""
    return datetime.datetime.now().isoformat(timespec="seconds")


def today_str() -> str:
    """Return today's date as YYYY-MM-DD."""
    return datetime.date.today().isoformat()


def unique_id() -> str:
    """Return a short unique ID string (first 8 chars of a UUID4)."""
    return str(uuid.uuid4())[:8]


def parse_json_safely(text: str):
    """
    Try to parse a JSON string and return the result as a dict.
    Returns None if parsing fails, so the caller can handle the error gracefully.
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
