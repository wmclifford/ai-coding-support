# Project Goals

> Machine-readable summary

```yaml
project:
  name: ai-coding-support
  vision: "Provide a meta-project framework and toolkit for creating, governing, and maintaining software projects with AI coding agents."
  primary_audience: [ "solo_developers", "small_teams" ]
  default_supported_stacks: [ "java", "python", "nodejs", "golang" ]
  initial_template: "nodejs"
  automation_default: "human_review_required"
  publishing_strategy: "publish_from_this_repo"
  license: "MIT"
  governance_approver_model: "owner-driven"
```

## Vision

Provide a meta-project framework and toolkit that teams (and AI agents) can use to consistently design, bootstrap,
govern, and maintain software projects that are developed with the help of AI coding agents. The project produces
opinionated but extensible governance documents, task schemas, agent prompt templates, CI workflow patterns, and
project templates that are safe, auditable, and easy to adopt.

## Purpose

- Standardize how AI agents are instructed, evaluated, and integrated into the software delivery lifecycle.
- Provide reusable artifacts (docs, schemas, templates, actions) that reduce friction when bootstrapping new projects
  and enforce auditability (evidence, task traceability).
- Make it simple for teams to adopt best-practices for security, code quality, and reproducible builds when using AI
  assistance.

## Primary audience

- Solo developers, small engineering teams, and early-stage product teams looking to incorporate AI-assisted
  development workflows.
- The governance is intentionally lightweight by default but can be extended for larger organizations.

## Scope

In-scope:

- Governance documents and templates for repo layout, commits, branches, PRs, and task evidence.
- Schemas for task files and other metadata that agents will consume and produce.
- Example project templates (initial focus: Node.js, Python, Java) and usage patterns for those templates.
- Machine-friendly prompt templates and example agent roles (spec-author, implementer, reviewer) — content to be
  created iteratively.
- Guidance and examples for CI workflows and how to invoke reusable GitHub Actions (Actions themselves may live in
  this repo or an external tooling repo; publishing strategy is configurable).

Out-of-scope (initially):

- Hosting or running production CI services; the repo provides workflows and actions, not hosted runners.
- Full enterprise policy automation (e.g., signed artifacts, formal compliance attestations) — these can be added via
  extensions/ADRs.

## Success metrics (measurable)

- Adoption: at least 2 internal projects bootstrapped from templates within 3 months.
- Coverage: governance docs for commits/branches/PRs, task schema, and CI examples completed (100%) for the MVP.
- Quality: Linting and basic validation enabled for all governance docs and templates; the tooling repo provides a task
  schema validator and is referenced by CI examples.
- Auditability: Each sample task demonstrates the Two-commit Evidence ritual and includes `evidence.commit` fields.
- Usability: First-time onboarding (clone -> bootstrap) completes within 15 minutes using provided README and scripts.

## Non-negotiables

- No secrets checked into source control.
- Task evidence (`evidence.commit` and `evidence.prUrl`) is recorded for all tasks (documentation, examples, and
  production).
- CI must include a secrets scan (e.g., gitleaks) on PRs that change templates or workflows.
- Conventional commits and the Two-commit Evidence ritual are the default workflow for task-driven changes.

## MVP features (minimum viable set)

1. Completed `docs/governance/*` set: `Conventions.md`, `Goals.md`, `System.md`, `ADR.md` with actionable content.
2. `schemas/task-file.schema.v0.1.json` (existing) validated and documented in `docs/` with examples.
3. At least one project template (the initial template will be `nodejs`) with a bootstrap README and minimal CI example.
4. Agent-friendly prompt templates (basic) for three roles: spec-author, implementer, reviewer (Markdown templates
   with examples).
5. Example Tasks under `examples/Tasks/` (already present per your note) demonstrating evidence ritual.
6. A short "Getting started" guide for bootstrapping a new project from this meta-repo.

## Architecture & integration points

- Artifacts produced by this repo:
  - Governance docs and templates (Markdown)
  - JSON/YAML schemas used by agents and validators
  - Example workflows (GitHub Actions workflow files) demonstrating how to call validators and actions
  - Prompt templates and agent role definitions
- Tooling strategy: validation and enforcement tooling (task-file validator, linters) live in a separate tooling repo
  and are referenced from this repo's example workflows (per your note).

## Invariants (rules to hold true)

- All task files must conform to the official schema version referenced in `schemas/` for that task.
- PRs that change governance, templates, or schemas must include task evidence and pass CI checks (lint, gitleaks,
  schema validation in example workflow).
- Prompt templates must include: role, expected input, expected output format, acceptance criteria, and at least one
  worked example.

## Roadmap (recommended)

0–3 months (MVP):

- Finalize `docs/governance/*` contents.
- Pick and ship one project template (confirm stack choice).
- Produce agent prompt templates for spec-author, implementer, reviewer.
- Document task schema and integrate examples in `examples/Tasks/`.

3–6 months:

- Add additional project templates (up to two more stacks).
- Provide example GitHub Actions or composite actions and an approach for publishing them.
- Implement a CLI bootstrap helper (script) referencing templates.

6–12 months:

- Harden governance for larger teams: ADR examples, versioning policy, extension points.
- Add migration/upgrade guidance for template consumers.
- Expand observability and security guidance (dependency scanning policy, signing recommendations).

## Acceptance criteria / Definition of Done for Goals

- `docs/governance/Goals.md` contains a clear vision, audience, scope, measurable success metrics, and a
  prioritized roadmap.
- The goals document includes machine-friendly summary metadata (the YAML block at the top) for agent consumption.
- The team (you) confirms supported stacks and automation defaults, or provides changes to the YAML summary.

## Risks & assumptions

- Assumption: tooling for validation and enforcement will live in a separate repo and be referenced by workflows here.
- Risk: if supported stacks are not prioritized, templates may drift; mitigate by picking 1–3 stacks for the MVP.
- Risk: too much automation without clear acceptance criteria may allow incorrect merges; default to human review
  unless explicitly configured otherwise.
