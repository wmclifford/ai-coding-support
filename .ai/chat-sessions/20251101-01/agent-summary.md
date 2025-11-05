# Session Summary — Initial Prompts & Instructions (3‑Pass Plan)

Date: 2025-11-01
Branch: feat/initial-prompts

## Goals

- Establish prompts and instructions for the 3-pass plan (spec, scaffold, stabilize) for this repository.
- Define artifact formats and schemas for each pass and document the end-to-end execution flow.
- Align governance (Conventional Commits scope, branch naming) with prompts/instructions and documentation.

## Key decisions & conventions

- 3-pass plan
  - Spec: produce planned diffs only, write spec artifacts, first commit contains the task file updated to
    `in_progress` plus artifacts after approval and branch creation.
  - Scaffold: apply planned diffs; commit per change using Conventional Commits; produce `scaffold.yaml` and
    `scaffold-report.md` and commit them.
  - Stabilize: run checks (linters emphasized for this repo), iterate small fixes, produce `stabilize.yaml` and
    `stabilize-report.md`, update the task to `in_review`, commit the task file, and open a PR.

- Artifacts & schemas (under `.ai/task-artifacts/<TASK-ID>/`)
  - Spec: `spec.yaml` (machine-readable; `schemas/spec-artifact.schema.v0.1.json`), `planned-diffs.md` (human)
  - Scaffold: `scaffold.yaml` (machine-readable; `schemas/scaffold-artifact.schema.v0.1.json`),
    `scaffold-report.md` (human)
  - Stabilize: `stabilize.yaml` (machine-readable; `schemas/stabilize-artifact.schema.v0.1.json`),
    `stabilize-report.md` (human)

- Conventional Commits
  - Scope reflects the component/slice (e.g., `docs`, `schemas`, `governance`, `templates/java`).
  - Task ID appears in the footer: `Refs: <TASK-ID>` (not as scope).
  - Use a single, clear subject line; wrap body at 100 chars; use bullets for body.

- Branch naming
  - `<type>/<TASK-ID>-<slug>`, e.g., `feat/CFG-001-add-config`. One slash only.

- Task evidence
  - `schemas/task-file.schema.v0.1.json` extended to allow `evidence.timestamp` (ISO-8601) and `evidence.branchName`.
  - Use OBJECT shape for `evidence.testSummary` when possible; for this repo, record linter results in `notes` and
    zero test counts.

- Commit message formatting (recurring issue)
  - Do NOT embed `\n` literals. Use multiple `-m` flags or a message file with `git commit -F` to ensure real
    linefeeds.
  - Prefer a temporary message file for complex multi-line commit messages to guarantee formatting and wrapping.

## Files created/updated (high level)

- Prompts: `.github/prompts/001-spec-pass.md`, `002-scaffold-pass.md`, `003-stabilize-pass.md`
- Instructions: `.github/instructions/001-spec-pass-instructions.md`, `002-scaffold-pass-instructions.md`,
  `003-stabilize-pass-instructions.md`
- Schemas: `schemas/spec-artifact.schema.v0.1.json`, `schemas/scaffold-artifact.schema.v0.1.json`,
  `schemas/stabilize-artifact.schema.v0.1.json`, `schemas/task-file.schema.v0.1.json` (evidence extensions)
- Docs: `docs/three-pass-plan.md` (complete end-to-end guide with sample session and Mermaid diagram), updated
  `docs/governance/Conventions.md` (scope, evidence fields)
- Session notes: `.ai/chat-sessions/002-initial-prompts/agent-notes.md` (decisions, addendums)

## How to run each pass

- Spec
  - Load: `.github/prompts/001-spec-pass.md` + `.github/instructions/001-spec-pass-instructions.md`
  - Provide the task file path when asked (e.g., `Tasks/CFG-001.yaml`)
  - Approve planned diffs; agent creates branch, updates task file to `in_progress`, commits task file + spec artifacts
    as first commit

- Scaffold
  - Load: `.github/prompts/002-scaffold-pass.md` + `.github/instructions/002-scaffold-pass-instructions.md`
  - Agent validates `spec.yaml`, applies diffs, commits per change (component scope + Refs footer), writes and commits
    scaffold artifacts

- Stabilize
  - Load: `.github/prompts/003-stabilize-pass.md` + `.github/instructions/003-stabilize-pass-instructions.md`
  - Agent validates `scaffold.yaml`, runs linters, writes and commits stabilize artifacts, updates task to `in_review`,
    commits task file, and opens PR

## Open items / next steps

- Commit-message validator (later task) to enforce Conventional Commits and line-wrapping rules.
- Template-specific stabilize prompts for language stacks (Java, Node, Python) with build/test steps and coverage.
- Dry-run exercise with a sample spec artifact to validate end-to-end flow.

## Session outcome

- All three passes (prompts + instructions) authored and aligned with governance.
- Schemas added to validate artifacts; task evidence schema extended.
- Three-pass plan documented with example and diagram.
- Commit message formatting pitfalls documented and mitigations recorded.

