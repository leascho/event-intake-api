# Architecture Notes

## Current target (Evening 1–3)

```text
Client (Postman/curl)
   │  POST /events            GET /events/{id}
   ▼                          ▼
HTTP API (API Gateway v2)
   ▼                          ▼
Lambda: handle_create_event   Lambda: handle_get_event
   │ validate → normalize
   │ structured log (event_id, result)
   ▼
DynamoDB table "events"
   key: event_id (uuid)
   attributes: payload, status (processed|rejected), received_at
```

## Design decisions (short version)

- **DynamoDB, not RDS**: single-entity writes and key-based reads; zero
  administration; matches the access pattern exactly.
- **Validation before storage**: the API contract promises a full list of
  invalid fields in one 400 response, so validation is all-at-once, not fail-fast.
- **Rejected events are stored too** (Evening 2): makes the endpoint
  debuggable — you can inspect what arrived, not just what passed.
- **Validator has no AWS imports**: keeps it unit-testable locally.

Longer reasoning will be added as decision records in `docs/decisions/`.

## Security checklist (fill in as you go)

- [ ] Lambda role limited to this table and these actions
- [ ] No secrets anywhere in the repo
- [ ] API access plan decided (open for the learning phase, documented why)
- [ ] Cleanup routine after each session
