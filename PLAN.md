# ai-coding-support — High-level Plan

## Purpose

This document captures a high-level, human-friendly plan for the ai-coding-support meta-repository. It lists the project
components, their purpose, and 2–3 prioritized milestones per component. Milestones are intentionally broad (epic-level)
so they can be expanded into task files in later sessions.

## Scope

Components covered:

- CI workflows
- Project templates (organized by language)
- Helper / support tools (separate repos expected)
- Documentation and governance

## How to use this plan

- Review milestones and agree on priorities.
- For each milestone, create a `Tasks/<TASK-ID>.yaml` and run the three-pass workflow (Spec → Scaffold → Stabilize).
- Revisit open questions; unresolved items are recorded as follow-ups under "Open Questions & TODOs."

---

## Components and Milestones

### 1) CI workflows

**Purpose:** Provide reusable, secure, and well-documented CI patterns for validating templates, schema changes,
documentation, and published artifacts. CI will also gate contributions to `docs/`, `templates/`, and `schemas/` per the
repo's contribution rules.

**Milestones:**

- **M1: Core CI templates** — Implement GitHub Actions workflows for linting, schema validation, and conventional commit
  checks. These workflows should be reusable across templates.
- **M2: Template-specific CI** — Create language-specific CI flows that can be included by projects bootstrapped from
  templates (e.g., Node.js: install → lint → test → publish-check; Python: venv → lint → test → package-check).
- **M3: Security & compliance gates** — Add secrets scanning (`gitleaks`), dependency scanning, and optional policy
  checks
  (e.g., required ADRs for deviations).

### 2) Project templates (by language)

**Purpose:** Provide minimal, well-documented starter projects for common language ecosystems; each template includes CI
wiring, README, prompts, and helper scripts to integrate with agent workflows.

**Languages and candidate project types (draft):**

- **Node.js**
  - CLI tool / library
  - Web service (Express/Fastify)
  - Serverless function template
- **Python**
  - Library / package (pyproject-based)
  - CLI tool (click; use argparse only for very simple scripts)
  - Data science/minimal notebook starter (optional)
- **Go**
  - HTTP microservice (std, chi, or gin)
  - Library module (semver-ready)
- **Java**
  - Maven/Gradle library
  - Spring Boot microservice (minimal)

**Milestones:**

- **M1:** Define canonical template types per language and select the first set to implement (target: 1–2 templates per
  language to start).
- **M2:** Implement template scaffolds with CI include files, prompts, and instruction examples for agent usage.
- **M3:** Provide a `templates/cli` helper or small generator (node-based or python) to create project instances from
  templates and wire local dev scripts.

### 3) Helper / support tools

**Purpose:** Small utilities that help with template creation, validation, agent runs, and CI steps. These may live in
`tools/` or separate repositories depending on complexity.

**Milestones:**

- **M1: Validation utilities** — a simple CLI (preferably minimal-dependency) to validate schemas, task files, and
  artifact
  shapes locally (used in CI).
- **M2: Template generator CLI** — a helper to instantiate templates, optionally applying repo-level conventions
  (license, CODEOWNERS, initial task file). Can be a small Node or Python script.
- **M3: Release & publishing helpers** — tools/scripts to perform package publish checks, draft releases, or create
  changelogs following Conventional Commits.

### 4) Documentation & governance

**Purpose:** Centralized guidance for contributors and agents; stable ADRs for decisions that diverge from existing
governance.

**Milestones:**

- **M1: Canonical docs** — ensure `docs/governance/Goals.md`, `Conventions.md`, and `System.md` are complete and
  referenced
  by templates and CI.
- **M2: Template usage guides** — per-template `README.md` with instructions for bootstrapping, agent usage, and CI
  expectations.
- **M3: ADRs & decision log** — lightweight ADR process implemented (template ADRs, acceptance workflow).

---

## First templates to implement (initial rollout)

Based on the priorities above (language order and use-case priorities), the following are proposed as the first
templates to implement. These will be the focus of the first milestone (`templates-define` → `templates-implement`):

- **Node.js (priority 1)**
  - CLI template (minimal entrypoint, argument parsing, README, CI include)
  - Library template (package-ready, semver guidance, CI include)
- **Go (priority 2)**
  - CLI template (single-binary layout, module / go.mod, CI include)
  - Library module template (module layout, versioning guidance)
- **Python (priority 3)**
  - Library/package template (pyproject.toml, test scaffold, CI include)
  - CLI template (click/argparse minimal example)
- **Java (priority 4)**
  - Library template (Maven/Gradle) — initially treated as copy/paste friendly; implement minimal scaffold later if
    demand rises

---

## CI specifics (applied policy)

- **CI provider:** GitHub Actions only.
- **Mandatory PR checks (must be included in `ci-core`):**
  - Linting (language-appropriate linters or markdown/lint for docs)
  - Schema validation (validate YAML/JSON against repository schemas in `schemas/`)
  - Secrets scanning (`gitleaks` or equivalent)
- **Medium-priority checks (recommended but can be rolled out after mandatory checks):**
  - Commit message format validation (Conventional Commits)
  - License header/license file checks

## Helper / support tools (policy)

- Each helper/support tool will live in its own repository (not inside this meta-repo). This allows independent
  versioning, packaging, CI, and publishing to GitHub Packages.
- Preferred runtimes for initial tools: Node.js and Go (choose depending on the tool's role and dependencies).
- Each tool repo should include:
  - A minimal CI pipeline for building/testing/publishing to GitHub Packages.
  - A `setup-*` style GitHub Action or `action.yml` where appropriate (e.g., `setup-node` or `setup-go` wrappers) so
    downstream projects can adopt the tool in CI with a standard action.

## Template opinionation and agent-first approach

- Templates should be intentionally minimal: governing documents (Goals/Conventions/System), CI includes, task
  templates (for the three-pass flow), and AI prompts/instructions. The intent is to provide a tiny, well-documented
  starting point that an AI agent can fully scaffold into a complete project using only the supplied documentation and
  prompts.
- Later we will add optional, opinionated variants (for users who prefer batteries-included starters) but these will
  be separate template variants.

## Default tooling choices (recommended defaults)

To reduce decision friction when agents scaffold projects from templates, the following default tooling is proposed
for v1 templates. These are recommendations and can be overridden per-template or per-user preference.

- **Linters & formatters (recommended defaults):**
  - Node.js: `eslint` + `prettier` (widely used; integrates with editor tooling)
  - Go: `golangci-lint` (aggregator that wraps many Go linters)
  - Python: `flake8` for linting; `black` for formatting
  - Java: `checkstyle` + `pmd` (you commonly include PMD in addition to Checkstyle)

- **CLI libraries (recommended defaults):**
  - Node.js: `yargs` (simple, minimal)
  - Go: `cobra` (common, feature-rich) or `urfave/cli` (widely used alternative) — templates may also include a `flag`-based minimal example for micro-CLIs
  - Python: `click` (you confirmed this preference)
  - Java: `picocli` (lightweight CLI library; optional for minimal Java templates)

- **Testing frameworks (recommended defaults):**
  - Node.js: `jest`
  - Go: built-in `testing` + table-driven tests (use `go test`)
  - Python: `pytest` (recommended)
  - Java: `JUnit 5` (as requested)

- **Packaging & build preferences:**
  - Node.js: `npm` + `package.json` (standard)
  - Go: Go modules via `go.mod`
  - Python: `poetry` (you prefer this)
  - Java: `Gradle` (you prefer this)

## Centralized GitHub Actions & action wrappers

- **Policy:** GitHub Actions and any `setup-*` or action wrappers that are intended to be reused by downstream
  templates and tools will live in this meta-repo (centralized) so we have a single source of truth for CI building
  blocks. Suggested locations:
  - Reusable workflow templates: `.github/workflows/` (e.g., `.github/workflows/ci-core.yml` or `ci-core.yml` includes)
  - Reusable action metadata (if we publish `action.yml` wrappers): `.github/actions/<action-name>/action.yml` or
    `actions/<action-name>/action.yml`.

## Brave searches & evidence

- Per your suggestion, I will run web searches to confirm common/suggested linters and CLI libraries for each language
  (Node.js, Go, Python, Java) and summarize findings in the session notes and/or next plan iteration.

## No Tasks created in this session

- Confirming: no `Tasks/*.yaml` files will be created during this planning session.

## Next steps (short term)

- Finalize this `PLAN.md` with any edits you provide.
- Update `.ai/plan.yaml` (done in parallel) to reflect these choices for machine-friendly consumption.
- In a follow-up session, convert prioritized milestones into `Tasks/<TASK-ID>.yaml` and run the three-pass workflow.

## Document history

- 2025-11-04 — Initial draft by AI agent in session `20251104-01`.
