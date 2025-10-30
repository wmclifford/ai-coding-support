# System-Level Instructions

## Security

- Secrets: never in repo. Source from env/secret store; fail fast if missing.
- Validation at boundaries: Bean Validation + centralized exception handling.
- CORS: default deny; allow only configured origins via profile properties.
- Auth: basic auth for v1; upgrade path to token-based (bearer) noted in ADR.

## Dependencies

- Spring Boot 3.x BOM; managed starters: webflux, validation, actuator, data-r2dbc.
- Database driver: r2dbc-postgresql
- Migrations via Flyway (JDBC) by deployment pipeline (Flyway CLI/Gradle plugin) before app rollout
  in each environment; `spring.flyway.enabled=false` or omit Flyway starter.
- Database schema compatibility check on boot; the schema version (e.g., from `flyway_schema_history`)
  must be >= app min required version (stored in config: `app.schema.minVersion`) - fail fast.
- springdoc-openapi for OpenAPI; problem-details for RFC 7807 mapping.

## Observability

- Actuator enabled; expose `/actuator/health` (readiness, liveness) and
  `/actuator/metrics` to internal network only.
- Structured logs (JSON-capable); include `traceId`/`requestId` in MDC.
- Access logs for API with minimal fields; no PII.
- Emit metric `repo.query.duration{method=...}` and log when > 200 ms.

## Performance

- All list endpoints must paginate (`page`/`size`, default=20, max=100).
- Add indexes for filter columns before releasing an endpoint.
- Apply `@Transactional(readOnly=true)` to read queries.
- Outbound calls (if any) must use timeouts (2 seconds) and circuit breaker.
- Reactive backpressure respected (Flux with bounded `limitRate` where needed).

## API Surface

- JSON only; errors conform to RFC 7807 via `@ControllerAdvice`.
- Versioned URI prefix `/v1` for all controllers.
- OpenAPI generated on build; serve `/v3/api-docs` and `/swagger-ui` in non-prod.

## CI/CD

- Build with Gradle; tasks: `test`, `integrationTest`, with the code coverage gate >= 80%.
- Static analysis: PMD/Checkstyle optional; secrets scan via `gitleaks`.
- Artifacts: publish test and coverage reports.
- PR checks: `commitlint`, `spotlessCheck` (`--no-configuration-cache`), tests, coverage gate, `gitleaks`.
- Optional: task status validator script (fails PR if task JSON has invalid state or missing evidence).
- Block merge on any failure.
- Backward-compatible migrations first, then deploy app; only later do destructive changes (two-phase).
  - Step: `flyway -url=... -user=... -locations=db/migration migrate`
  - Step: smoke test against the migrated DB using Testcontainers or env DB
  - Deploy app only if migration + smoke pass

## Branch & Merge Policy

- PR is required to merge to `main` (and `develop`, if using GitFlow).
- **Trunk:**
  - require squash merges
  - PR title must be a Conventional Commit
  - include `Refs: [TASK-ID]` in PR body.
- **GitFlow (teams using `develop`):**
  - allow merge commits on `develop` (`commitlint` ignores merges)
  - releases squash into `main`
- Every PR references a **Task ID** in the body (same [TASK-ID] as in commits).
- CI must pass.
- Code review is required.

## Evidence & Audit

- Completed tasks must have `evidence.commit` set to the code SHA present in the repository.
- Optional: `evidence.prUrl` should point to the PR for audit trail (especially under squash).

## Data

- Postgres as primary store; Flyway migrations in `db/migration`.
- R2DBC for runtime access; prefer repository methods or `R2dbcEntityTemplate` for
  custom queries.
- Test data isolated via Testcontainers; never rely on local dev DB in CI.
