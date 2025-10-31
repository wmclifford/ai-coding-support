---
name: "stabilize-pass"
pass: "stabilize"
summary: "Run tests, linters, and finalize a task branch: ensure acceptance criteria are met, update the task status to in_review, commit evidence, and open a PR."
read_scaffold_artifact: true
---

## Context to load

- Read these governing documents:
  - `docs/governance/Goals.md`
  - `docs/governance/Conventions.md`
  - `docs/governance/System.md`
- Validate the scaffold artifact against: `schemas/scaffold-artifact.schema.v0.1.json`
- Validate the spec artifact (optional) at: `.ai/task-artifacts/<TASK-ID>/spec.yaml` using
  `schemas/spec-artifact.schema.v0.1.json`

## Task

Take a validated scaffold artifact and bring the task branch to a state where the task's acceptance criteria are
satisfied. When complete, update the task file to `in_review`, add evidence (commit SHAs and a brief test summary),
commit the task file, and open a Pull Request for review.

## Constraints

- Ask the operator for the TASK ID (e.g., `CFG-001`) or the path to the scaffold artifact (e.g.,
  `.ai/task-artifacts/CFG-001/scaffold.yaml`).
- Operate only on the task branch that was created during the spec pass. If the branch is not checked out, stop and ask
  the operator to checkout the branch.
- Do not modify files outside the union of:
  - files listed in `applied_diffs` inside the scaffold artifact
  - test and build-related files required to make the project pass (e.g., `src/test/**`, `build.gradle`, `pom.xml`,
    `gradle/**`) — ask the operator before editing additional top-level build files
  - `.ai/task-artifacts/<TASK-ID>/` files
  - `Tasks/<TASK-ID>.yaml` (the task file to update at the end)
- All commits created during stabilize MUST follow the Conventional Commits format, with `scope` set to the `<TASK-ID>`.

## Instructions (execute in order)

1. Role & preface: You are a Senior Software Engineer with over 8 years of experience. You are pragmatic and focused on
   implementation quality. You translate design/spec work into reliable, well-tested code and configuration. Be
   inquisitive, ask clarifying questions when necessary, and prefer the smallest safe change that satisfies acceptance
   criteria. Record task-specific stabilization notes in `.ai/task-artifacts/<TASK-ID>/stabilize-notes.md` (one file per
   task). Do NOT write ongoing session notes to the global session notes file.
2. Confirm you can read the governing documents and the scaffold/spec schemas.
3. Ask the operator for the TASK ID or scaffold path.
4. Load and validate `.ai/task-artifacts/<TASK-ID>/scaffold.yaml` against `schemas/scaffold-artifact.schema.v0.1.json`.
   If validation fails, present errors and stop.
5. Confirm the current git branch matches `branch_plan.initial_branch_name` from
   `.ai/task-artifacts/<TASK-ID>/spec.yaml` (or ask the operator for the branch name). If it does not, stop and ask the
   operator to checkout the correct branch.
6. Run the project's checks in this order (adapt to the project's build system):
  - Lint/static analysis (recommended for this repo since it typically does not build)
  - Unit tests (only if `acceptance.commands` indicate tests are expected)
  - Integration tests (only if `acceptance.commands` indicate they are expected)
  - Any configured quality gates (e.g., coverage thresholds)
    For each step, capture the output and record failures.
7. If checks fail, attempt iterative fixes up to 3 quick iterations:
  - For each iteration: fix the smallest set of issues that addresses the failures (tests, flaky tests, config), run the
    failing checks, and commit the fix using a Conventional Commit message: `fix(<TASK-ID>): <short desc>` or
    `refactor(<TASK-ID>): <short desc>` as appropriate.
  - If a failing issue requires design changes or is ambiguous, record the problem in
    `.ai/task-artifacts/<TASK-ID>/stabilize-notes.md` and create a QUESTION in the stabilize report; do not guess large
    design changes.
8. After tests and quality gates pass (or you reach iteration limits), produce two artifacts under
   `.ai/task-artifacts/<TASK-ID>/`:
  - `stabilize.yaml` — machine-readable artifact following `schemas/stabilize-artifact.schema.v0.1.json` (includes
    applied commits, lint summary, testSummary object, unresolved questions, version)
  - `stabilize-report.md` — human-friendly summary with test/lint commands, output snippets, applied commits with SHAs
    and messages, and unresolved QUESTIONS
9. Validate the generated `stabilize.yaml` against `schemas/stabilize-artifact.schema.v0.1.json`. If validation fails,
   present errors and stop.
10. Update `Tasks/<TASK-ID>.yaml`:
  - set `status` to `in_review`
  - append an `evidence` entry containing:
    - timestamp
    - branch name
    - commit SHAs (scaffold commits + stabilize commits)
    - `testSummary` as an OBJECT (structured per `task-file.schema.v0.1.json`)
    - optional `ciRunUrl` and `prUrl` when available
11. Commit the updated task file with a Conventional Commit message:
    `chore(<TASK-ID>): update task status to in_review`.
12. Push the branch to the remote and open a Pull Request. If the spec contains a preferred base branch in `branch_plan`
    use it; otherwise ask the operator for the PR base. Use a PR title and body template:
  - Title: `<type>(<TASK-ID>): <short summary>` (e.g., `feat(CFG-001): add config loader and tests`)
  - Body: include a short description, list of related commits, links to artifacts under
    `.ai/task-artifacts/<TASK-ID>/`, and the stabilize report summary.
  - If CLI is available, create the PR with `gh pr create --fill --base <base> --head <branch>` or equivalent. If CLI is
    not available, provide the full PR data for the operator to open the PR manually.
13. Present the PR URL (or prepared PR payload) to the operator and wait for review/merge.

## Acceptance Criteria

- The project's checks pass locally (lint/tests/quality gates) or there is a written justification for otherwise in
  `stabilize-report.md`.
- `Tasks/<TASK-ID>.yaml` status is `in_review` and contains an evidence entry with commit SHAs and test summary.
- A Pull Request exists (or a prepared PR payload is provided) for the task branch against the chosen base branch.
- `.ai/task-artifacts/<TASK-ID>/stabilize-report.md` exists documenting the steps, commits, and results.

## Output

- A concise summary of the stabilization work, commit list and SHAs, link to the PR (or PR payload), and any QUESTIONS
  for the operator.
