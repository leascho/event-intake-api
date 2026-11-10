# Event Intake API

A small serverless integration endpoint on AWS. It receives synthetic HR onboarding
events (like an external system webhook), validates them, stores them in DynamoDB,
and serves them back by ID.

Built as a learning project to transfer enterprise integration patterns
(validation, error handling, structured logging, reproducible infrastructure)
from Workday integrations to AWS.

> **Data policy:** this project uses **synthetic data only**. Never send real
> employee, customer, or company data through it.

## Architecture

```text
POST /events          GET /events/{id}
      │                      │
      ▼                      ▼
   API Gateway  ──────►  Lambda  ──────►  DynamoDB
                        (validate,
                         transform,
                         log)
```

- **API Gateway** — HTTP API entry point
- **Lambda** — validates the payload, enriches it, writes structured logs
- **DynamoDB** — stores each event with a status (`processed` / `rejected`)

## Status

Work in progress — see the [roadmap](#roadmap). Currently at the skeleton stage:
project structure, validator, and tests are in place; the AWS wiring is the next step.

## Repo layout

```text
app/                Lambda code (handler, validator)
tests/              Unit tests (run without AWS)
infrastructure/     Terraform (currently a placeholder)
docs/               Architecture notes and decision records
.github/workflows/  CI: runs the unit tests on every push
```

## API contract (planned)

### POST /events

```json
{
  "employee_id": "EMP-0001",
  "first_name": "Alex",
  "last_name": "Sample",
  "email": "alex.sample@example.com",
  "start_date": "2027-01-15",
  "department": "Integration"
}
```

- `200` — event accepted and stored
- `400` — validation failed, response lists every invalid field

### GET /events/{id}

- `200` — the stored event, including its status
- `404` — unknown ID

## Local development

```bash
pip install -r requirements-dev.txt
pytest
```

The unit tests run entirely locally — no AWS account needed.

## Cleanup reminder

Anything created in a personal AWS account while working on this project should be
removed (or its cost checked) at the end of each session. DynamoDB on-demand is
cheap, but the habit matters.

## Roadmap

- [x] Repo structure, validator, unit tests, CI
- [ ] Evening 1 — working endpoint via AWS console (table, function, HTTP API)
- [ ] Evening 2 — error handling, structured logging, status field
- [ ] Evening 3 — harden tests, document API behavior, polish README
- [ ] Evening 4 — replace manual setup with Terraform
- [ ] Later — IAM role hardening, GitHub Actions deployment via OIDC
