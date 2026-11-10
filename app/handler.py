"""Lambda handler for the Event Intake API.

Two entry points (both still TODO — wire them up in Evening 1):

- POST /events   -> handle_create_event
- GET /events/id -> handle_get_event

The validation logic lives in app/validator.py so it stays testable
without AWS. Keep this module about wiring (parsing the event,
calling the validator, mapping results to HTTP responses), not about
business rules.
"""

import json
import logging
import uuid
from datetime import datetime, timezone

from app.validator import ValidationError, validate_event

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _response(status: int, body: dict) -> dict:
    return {"statusCode": status, "body": json.dumps(body)}


def handle_create_event(apigw_event: dict, context) -> dict:
    """POST /events — validate, store, respond.

    TODO (Evening 1):
      1. Parse the JSON body (reject invalid JSON with 400).
      2. Call validate_event().
      3. Generate an event_id (uuid4) and received_at timestamp.
      4. Store the item in DynamoDB (status="processed").
      5. Return 200 with the event_id.
    TODO (Evening 2):
      - Log event_id, validation result and outcome as structured JSON.
      - Store rejected events with status="rejected" instead of dropping them.
    """
    logger.info("create event received: %s", json.dumps(apigw_event.get("body", "")))
    try:
        payload = json.loads(apigw_event.get("body") or "{}")
    except json.JSONDecodeError:
        return _response(400, {"error": "invalid JSON"})

    try:
        validated = validate_event(payload)
    except ValidationError as exc:
        return _response(400, {"error": "validation failed", "fields": exc.errors})

    event_id = str(uuid.uuid4())
    received_at = datetime.now(timezone.utc).isoformat()
    # TODO: put_item into DynamoDB here.
    logger.info("event %s validated for %s", event_id, validated["employee_id"])
    return _response(200, {"event_id": event_id, "received_at": received_at,
                           "status": "validated (storage not wired yet)"})


def handle_get_event(apigw_event: dict, context) -> dict:
    """GET /events/{id} — return a stored event.

    TODO (Evening 1): read the item from DynamoDB by path parameter id,
    return 200 with the item or 404 if it does not exist.
    """
    event_id = apigw_event.get("pathParameters", {}).get("id")
    if not event_id:
        return _response(400, {"error": "missing event id"})
    return _response(501, {"error": "not implemented yet"})
