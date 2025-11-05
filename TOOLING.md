# ai-coding-support — Tooling Defaults (quick reference)

This single-file summary lists the default tooling choices used as the baseline for v1 templates and CI wiring.
It is intentionally concise — use it as a quick reference when creating or reviewing templates.

## Scope

- Languages: `Node.js`, `Go`, `Python`, `Java`
- Focus: CLI → library → web services
- CI provider: GitHub Actions (centralized reusable workflows in this repo)

## Mandatory PR checks (ci-core)

The `ci-core` reusable workflow should include these mandatory checks for pull requests:

- `lint`
- `schema-validation`
- `gitleaks`

## Medium-priority checks (recommended)

- `conventional-commit-check`
- `license-check`

## Default tooling by language

Below are the recommended defaults for each language. These are suggestions to reduce decision friction; templates
may override them as needed.

### Node.js

- Linters & formatters: `eslint` + `prettier`
- CLI library: `yargs`
- Test framework: `jest`
- Packaging: `npm` (`package.json`)

### Go

- Linters: `golangci-lint` (aggregator for `govet`, `staticcheck`, etc.)
- CLI libraries: `cobra` (primary), `urfave/cli` (light alternative)
- Test framework: `go test` (built-in)
- Packaging: Go modules (`go.mod`)

### Python

- Linters & formatters: `flake8` + `black` (note: `ruff` is a fast alternative)
- CLI library: `click`
- Test framework: `pytest`
- Packaging/build: `poetry` (`pyproject.toml`)

### Java

- Linters/static analysis: `checkstyle` + `pmd` (SpotBugs optional)
- CLI library: `picocli`
- Test framework: `JUnit 5`
- Build tool: `Gradle`

## Helper & support tools policy

- Tools live in separate repositories (not in this meta-repo). This allows independent versioning and releases.
- Preferred runtimes: Node.js and Go depending on the tool's needs.
- Each tool repository should include:
  - a minimal CI pipeline for build/test/publish
  - a `setup-*` style GitHub Action or `action.yml` if the tool is intended to be consumed as a reusable action
- Reusable Actions and workflow templates are centralized in this meta-repo under either:
  - `.github/workflows/` (reusable workflow templates), and
  - `.github/actions/` or `actions/` (action metadata like `action.yml`).

## Notes

- These defaults are recommendations to reduce decision friction for agents and contributors. Templates may override
  them per project needs.
- Publishing automation is deferred to per-template planning (Option A in the plan).

---

## Document history

- 2025-11-04 — Tooling defaults summary created/beautified in session `20251104-01`.
