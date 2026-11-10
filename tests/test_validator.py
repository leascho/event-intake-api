"""Unit tests for the event validator — run locally, no AWS needed."""

import pytest

from app.validator import ValidationError, validate_event


def valid_event() -> dict:
    return {
        "employee_id": "EMP-0001",
        "first_name": "Alex",
        "last_name": "Sample",
        "email": "alex.sample@example.com",
        "start_date": "2027-01-15",
        "department": "Integration",
    }


def test_valid_event_passes():
    result = validate_event(valid_event())
    assert result["employee_id"] == "EMP-0001"
    assert result["department"] == "Integration"


def test_missing_required_fields_are_all_reported():
    with pytest.raises(ValidationError) as excinfo:
        validate_event({})
    errors = excinfo.value.errors
    for field in ("employee_id", "first_name", "last_name",
                  "email", "start_date", "department"):
        assert field in errors


def test_bad_date_format_is_rejected():
    event = valid_event()
    event["start_date"] = "15.01.2027"
    with pytest.raises(ValidationError) as excinfo:
        validate_event(event)
    assert "start_date" in excinfo.value.errors


def test_non_dict_payload_is_rejected():
    with pytest.raises(ValidationError):
        validate_event(["not", "an", "object"])


def test_values_are_trimmed():
    event = valid_event()
    event["first_name"] = "  Alex  "
    result = validate_event(event)
    assert result["first_name"] == "Alex"
