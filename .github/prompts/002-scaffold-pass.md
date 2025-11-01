---
name: "scaffold-pass"
pass: "scaffold"
summary: "Apply the planned diffs from a spec artifact and produce a scaffold report."
read_spec_artifact: true
---

## Context to load

- Read these governing documents:
  - `docs/governance/Goals.md`
  - `docs/governance/Conventions.md`
  - `docs/governance/System.md`
- Validate the machine-readable spec against: `schemas/spec-artifact.schema.v0.1.json`

## Task

Take a previously-approved spec artifact and apply the planned diffs to the repository. Produce a short scaffold report
documenting applied diffs and commit SHAs.

## Constraints

- Ask the operator for the TASK ID (e.g., `CFG-001`) or the path to the spec artifact (e.g.,
  `.ai/task-artifacts/CFG-001/spec.yaml`).
- Do not modify files outside of the union of:
  - files listed in `planned_diffs` inside the spec artifact
  - the `.ai/task-artifacts/<TASK-ID>/` directory
- The scaffold pass must run on the task branch—that branch must already exist and be checked out by the agent. If not,
  stop and request the branch name.
- All commits created by the scaffold pass MUST follow the Conventional Commits format, with `scope` set to the
  `<TASK-ID>` (e.g., `feat(CFG-001): ...`).

## Instructions (execute in order)

1. Confirm you can read the governing documents and the spec schema.
2. Ask the operator for the TASK ID or spec path.
3. Load and validate the spec artifact at `.ai/task-artifacts/<TASK-ID>/spec.yaml` against
   `schemas/spec-artifact.schema.v0.1.json`. If validation fails, present errors and stop.
4. Confirm the current git branch matches `branch_plan.initial_branch_name` from the spec. If it does not, stop and ask
   the operator to checkout the correct branch.
5. For each entry in `planned_diffs` (in order):
  - If `change` == `add`: create the file and insert the content or marker-specified addition. If no content is provided
    in the spec, create a clear placeholder with a TODO and a short comment explaining what's expected.
  - If `change` == `modify`: locate the `marker` in the target file. If the marker is clear, apply the modification
    inline. If the marker is ambiguous or missing, do NOT guess; instead add a TODO marker in the file and record a
    question in the report.
  - If `change` == `delete`: remove the file.
  - If `change` == `rename`: rename the file as specified (include both old and new paths in the spec's `file` field; if
    missing, record a question and skip).
  - After applying each file change, stage and commit the change with a Conventional Commit message:
    `type(<TASK-ID>): subject` (choose `type` per the scaffold instructions and include a short `—` separated
    description if helpful).
6. After all diffs are processed, write two artifact files under `.ai/task-artifacts/<TASK-ID>/`:
  - `scaffold.yaml` (machine-readable) containing applied diffs and their commit SHAs
  - `scaffold-report.md` (human-friendly) containing:
    - summary header (task_id, author, created_at from spec)
    - list of applied diffs with commit SHA for each
    - any QUESTIONS or unresolved markers
    - timestamp and agent identity
7. Stage and commit the scaffold artifacts with a Conventional Commit message:
   `chore(<TASK-ID>): add scaffold artifacts`.
8. Present a concise summary to the operator with the list of commits and any QUESTIONS. Wait for operator review before
   proceeding to stabilize.

## Acceptance Criteria

- All planned diffs from the validated spec were applied or explicitly recorded as unresolved.
- Each applied diff produced a separate Conventional Commit with a descriptive message that includes the `<TASK-ID>` as
  the scope.
- `.ai/task-artifacts/<TASK-ID>/scaffold.yaml` and `.ai/task-artifacts/<TASK-ID>/scaffold-report.md` exist and document
  applied diffs, commit SHAs, and questions.
- No files outside the allowed set were modified.

## Output

- A brief summary listing the commits created and any QUESTIONS that need operator input.
