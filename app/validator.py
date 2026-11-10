"""Payload validation for incoming HR onboarding events.

Kept deliberately free of AWS imports so it can be unit-tested locally.

Status: basic skeleton. Extend the rules as the project grows —
each rule you add should come with a test in tests/test_validator.py.
"""

from datetime import datetime
from typing import Any, Optional


class ValidationError(Exception):
    """Raised when an event fails validation. Carries all errors at once."""

    def __init__(self, errors: dict[str, str]):
        super().__init__("; ".join(f"{k}: {v}" for k, v in errors.items()))
        self.errors = errors


def _require_string(event: dict[str, Any], field: str, errors: dict[str, str]) -> None:
    value = event.get(field)
    if not isinstance(value, str) or not value.strip():
        errors[field] = "required and must be a non-empty string"


def validate_event(event: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic onboarding event and return a normalized copy.

    Raises ValidationError with a field -> message mapping on failure.
    """
    if not isinstance(event, dict):
        raise ValidationError({"payload": "must be a JSON object"})

    errors: dict[str, str] = {}
    for field in ("employee_id", "first_name", "last_name", "email", "department"):
        _require_string(event, field, errors)

    # start_date: required, ISO format YYYY-MM-DD
    start_date: Optional[str] = event.get("start_date")
    if isinstance(start_date, str) and start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            errors["start_date"] = "must be an ISO date string YYYY-MM-DD"
    else:
        errors["start_date"] = "required and must be a non-empty string"

    if errors:
        raise ValidationError(errors)

    # Normalized copy — only fields we know and validated.
    return {
        "employee_id": event["employee_id"].strip(),
        "first_name": event["first_name"].strip(),
        "last_name": event["last_name"].strip(),
        "email": event["email"].strip(),
        "start_date": start_date,
        "department": event["department"].strip(),
    }
