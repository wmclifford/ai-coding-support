# Coding Conventions

## Code Structure

- Framework: Spring Boot 3.x; DI via `@Component`/`@Service`/`@Repository` only.
- Modules: `customer`, `shared`, `config`. Public API surface lives in `api` packages;
  domain in `service`/`domain` packages; data adapters in `data`.
- Controllers never call R2DBC directly; all persistence via services -> repositories.
- Configuration via `@Configuration` and `@ConfigurationProperties` under `config`.
- No static singletons; configuration via Spring `@Configuration` + profiles.
- Use reactive stack end-to-end; prefer reactive controller/service signatures.

## Naming & Packaging

- Packages: `io.github.wmclifford.<app>.<layer>.<feature>` (e.g., `...api.customer`).
- Class names reflect layer: `*Controller`, `*Service`, `*Repository`, `*Mapper`.
- DTOs end with `Request`/`Response`; entities without suffix.
- Configuration classes live in `...config`.

## API

- JSON over HTTP; error model: RFC 7807 using Spring `ProblemDetail`.
- Pagination for list endpoints: query params `page`, `size` (default=20, max=100).
- API versioning via URI prefix `/v1/`.
- OpenAPI annotations required for controllers; describe pagination parameters.

## Validation & Security

- Input validation: Bean Validation annotations + `@Validated` on controller.
- No secrets in repo; configuration via env/profiles; forbid plaintext credentials in `application.yml`.
- Sanitized logging for inputs/headers; never log PII or credentials.

## Data-Access (R2DBC)

- Use Spring Data R2DBC repositories; prefer method queries or `@Query` with bounds;
  return reactive types where applicable.
- All repository reads that can list results must paginate (Pageable); <= 100 results.
- Read models use projections/DTOs; avoid exposing entities directly to API.
- Migrations via Flyway; every schema change stored in `db/migration`.

## Testing

- JUnit 5; Mockito for units; SpringBootTest only for slice/integration.
- AssertJ for assertions; custom assertion classes for entities/projections/DTOs (`*Assertion`).
- Line coverage >= 80% (JaCoCo). Critical branches are covered.
- Test naming: `should<Expected>_when<Condition>()`.
- Integration tests use Testcontainers Postgres; tag with `@Tag("integration")`.
- Separate source set: `src/integrationTest/java` with its own task `integrationTest`.

## Observability & Logging

- Actuator enabled with `/actuator/health` exposed.
- Request-id (correlation) required: log on entry/exit; propagate in MDC.
- Structured logging via SLF4J; no `System.out`/`printStackTrace`.

## Build & CI

- Build: `./gradlew clean build`; checks: tests + coverage + (optional) PMD/Checkstyle.
- Coverage gate: fail if < 80%
- Lint rules auto-fix where possible; remaining violations block PR.

## Formatting

- Source of truth: `.editorconfig`.
- Enforced via Spotless (Java + Prettier for JSON/YAML/MD).
- Commands:
  - Format: `./gradlew --no-configuration-cache spotlessApply`
  - Check (CI): `./gradlew --no-configuration-cache spotlessCheck`
- Agents must run formatting after edits and re-stage only formatted files.

## Commits & Branches

- **Conventional Commits** required; header lower-case; body bullets wrapped at 100 chars; task
  reference goes in the footer as `Refs: [CATEGORY-NNN]`.
  - Format:
    - **Header:** `<type>(<scope>): <summary>`
    - **Body:** `<blank line> <body>` (optional)
    - **Footer:** `<blank line> <footer> [<TASK-ID>]`
  - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
  - Scope: short area like `api`, `service`, `data`, `config`, `obs`
  - [TASK-ID]: the category ID, e.g. `[PAG-002]`
  - Use `!` after scope to mark breaking change, per spec: `feat(api)!: ...`
- **Two-commit evidence ritual:**
  1. CODE commit implements the task,
  2. EVIDENCE commit updates `Tasks/<ID>.json` with `"evidence.commit" = <code SHA>`.
- **One task per PR** preferred; avoid mixing concerns.
- Branch Naming:
  - Trunk: `feat/<TASK-ID>-<slug>`
  - GitFlow: `feature/<TASK-ID>-<slug>`
- Agents must create/checkout branch after spec approval and before edits.
- Merging:
  - Local: linear history per task (rebase or squash locally).
  - Remote: **squash merges** recommended; PR title must follow Conventional Commits.

## Task Lifecycle (cheat sheet)

`pending` -> `in_progress` (branch created) -> `review` (PR opened) -> `done` (merged + evidence commit present)

## Templates

- Commit message template: `docs/commits/.gitmessage`
- PR template: `.github/pull_request_template.md` (include `Refs: [TASK-ID]` in footer)

## Documentation

- Keep README up to date (run, test, build steps).
- Generate and publish OpenAPI (springdoc) as part of the build.

## Deviations

- Any deviation must include a short ADR entry with rationale and consequences.
