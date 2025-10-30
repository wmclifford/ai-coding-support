# Project Goals

## Overview

A lightweight CRUD + search service for managing customer records for internal operations.
V1 delivers create/read/update/delete and server-side pagination with basic auth.

## Non-Negotiables

- Language/Build: Java 21; Gradle.
- Framework: Spring Boot 3.x (application runtime, DI, actuator).
- API: JSON over HTTP; errors conform to RFC 7807.
- Testing: ≥ 80% line coverage; TDD preferred.
- Data: schema migrations via Flyway; no untested ad-hoc SQL.
- Security: no secrets in repo; validate inputs at boundaries.
- Observability: /health endpoint, basic metrics, request-id logs.
- CI: PRs must pass build, tests, and coverage gate.

## Architecture

- Shape: Layered (API → Service → Data).
- Boundaries:
  - API: HTTP controllers, JSON I/O, RFC 7807 error mapping.
  - Service: domain orchestration, validation, invariant enforcement.
  - Data Access: R2DBC repository adapters targeting Postgres; Flyway migrations.
  - Modules: customer (domain), shared (common utilities/types).

## Invariants

- All list endpoints paginate (default 20, max 100).
- Outbound calls use timeouts (2s) and map failures to RFC 7807 responses.
