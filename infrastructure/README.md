# Infrastructure (Terraform)

This directory will hold the Terraform definition of the project, replacing the
manual AWS console setup from Evening 1.

Planned resources:

| Resource | Purpose |
|---|---|
| `aws_dynamodb_table` | Event store (on-demand billing, single hash key `event_id`) |
| `aws_lambda_function` | Handler from `app/` |
| `aws_apigatewayv2_api` + integration + route | HTTP API `POST /events`, `GET /events/{id}` |
| `aws_iam_role` + policy | Least-privilege Lambda execution role (DynamoDB `PutItem`/`GetItem` only) |

Until then, the manual setup steps are documented in `docs/labs/`.

Guiding rules for this project:

- The Lambda role gets only the actions it needs, on only this table.
- No secrets in code or state — nothing in this project needs any.
- `terraform destroy` must cleanly remove everything `terraform apply` created.
