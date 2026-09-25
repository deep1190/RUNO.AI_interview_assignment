
"""Configuration for historical CRM dataset demonstrations."""

import os
from datetime import date
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def is_demo_mode() -> bool:
    """Return whether historical-data demonstration mode is enabled."""
    return os.getenv("DEMO_MODE", "false").strip().lower() in {
        "true",
        "1",
        "yes",
        "on",
    }


def get_reference_date() -> date:
    """
    Return the date used to interpret relative date expressions.

    Normal mode: actual current date.
    Demo mode: configured historical reference date.
    """
    if not is_demo_mode():
        return date.today()

    raw_date = os.getenv("DEMO_REFERENCE_DATE", "").strip()

    if not raw_date:
        raise ValueError(
            "DEMO_REFERENCE_DATE must be set when DEMO_MODE=true."
        )

    try:
        return date.fromisoformat(raw_date)
    except ValueError as exc:
        raise ValueError(
            "DEMO_REFERENCE_DATE must use YYYY-MM-DD format."
        ) from exc


def get_demo_metadata() -> dict:
    """Provide transparent information about date interpretation."""
    reference_date = get_reference_date()

    return {
        "demo_mode": is_demo_mode(),
        "reference_date": reference_date.isoformat(),
    }
