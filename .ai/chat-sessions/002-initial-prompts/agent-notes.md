# Session notes — Initial adoption of agent-instructions

Date: 2025-10-31

Summary:

- I have loaded and will follow the instructions in `.ai/chat-sessions/002-initial-prompts/agent-instructions.md` for
  this session. That file designates the role (Principal Architect), the governing documents to consult, and the
  objectives/constraints for creating prompts and agent instructions.

Key directives I will follow from the instructions:

- Record notes for this session in this file (`.ai/chat-sessions/002-initial-prompts/agent-notes.md`).
- Create a prompt for each pass of the 3-pass Plan (spec, scaffold, stabilize) and place prompts in `.github/prompts/`.
- Place agent instruction files in `.github/instructions/` when necessary.
- Process each prompt/instruction file individually following the 3-pass plan.
- Ask clarifying questions before completing the spec pass.
- Keep prompts concise (guideline: <100 lines) and include required sections (YAML header, Context, Task, Constraints,
  Instructions, Acceptance Criteria, Output).

Assumptions (inferred where not explicit):

1. The repository root is the workspace and the branch for this work has already been created (as noted in the
   instructions). I'll not create branches unless you ask me to — I'll instead list the branch name I'll use for
   approval.
2. We should not modify files outside `.github/prompts/` and `.github/instructions/` for this task unless you explicitly
   permit it.

Questions for you (needed before I begin the spec pass):

1. Confirm branch policy: do you want me to create and switch to a branch per prompt (e.g.,
   `feature/ai/prompts/002-initial-prompts`) or use an existing branch you mentioned? If yes, should I create the branch
   now and include the branch name in the task outputs? (If you prefer to create branches yourself, say so and I'll only
   list the branch I would use.)

2. For the prompts we create: do you want separate prompt files for the three passes (spec, scaffold, stabilize) per
   task (i.e., three files per task), or one prompt file that describes the entire 3-pass plan and is executed three
   times? My recommendation is one prompt per pass to keep responsibilities small and testable, but I'll follow your
   preference.

Next steps after you answer:

- Draft the spec-pass prompt file in `.github/prompts/` for the initial prompt set and a companion agent instruction
  file in `.github/instructions/`, then present the planned diffs and tests to you for approval (per the 3-pass
  process).
- Wait for approval before proceeding to scaffold.

Progress: updated notes file with the above. Waiting on your answers to the two questions before the spec pass.

---

## Discussion: spec-pass output, handoff to scaffold, and end-to-end usage

Decision summary:

- Short answer: publish the spec both to the chat (human-readable) and to a machine-readable working file so the
  scaffold pass can read and act on it programmatically.
- Recommended working-file location: `.ai/task-artifacts/<TASK-ID>/spec.yaml` and a companion human-readable
  planned-diffs file at `.ai/task-artifacts/<TASK-ID>/planned-diffs.md`.
- Rationale: chat-only output is fine for manual review, but writing a stable, machine-readable artifact enables
  reproducible automation, easier review, and a clean handoff to the scaffold pass (the scaffold agent can parse the
  YAML and apply the planned diffs). The artifact is also helpful for audits and for CI if we want to gate automation.

Machine-readable spec (recommended minimal schema):

- YAML top-level fields (example `spec.yaml`):
  - task_id: CFG-001
  - author: <agent-or-operator>
  - created_at: 2025-10-31T12:34:56Z
  - acceptance_criteria: |
    One-paragraph summary pulled from Tasks/CFG-001.yaml
  - branch_plan:
    - branch_name_pattern: "<type>/<task-id>-<slug>"
    - initial_branch_name: "feat/CFG-001-add-config"
    - first_commit_file: "Tasks/CFG-001.yaml"
    - first_commit_message: "spec pass: branch created"
  - planned_diffs: # list of changes to apply
    - file: "src/main/resources/application.yml"
      change: "add"
      marker: "append new property under 'app.config:'"
      justification: "satisfies acceptance criterion X"
    - file: "src/main/java/com/example/config/ConfigLoader.java"
      change: "modify"
      marker: "add method 'loadFromEnv' after class declaration"
      justification: "satisfies acceptance criterion Y"
  - questions: []

- Companion `planned-diffs.md` should contain the same planned diffs in human friendly form and a small unified-diff
  sketch or clear edit markers so reviewers can visualise the change quickly.

Why not store specs under `.github/`?

- Keep `.github/` focused on CI and prompts/instructions; keep task artifacts under `.ai/` so they are clearly agent
  artifacts and don't interfere with repository configuration or CI rules.

## How the prompts & instructions are used end-to-end (example: process `Tasks/CFG-001.yaml`)

Checklist (high-level):

1. Spec pass (interactive)

- Agent reads governing docs
- Agent asks operator for task file path (e.g., `Tasks/CFG-001.yaml`)
- Agent reads the task file and summarizes acceptance criteria
- Agent produces a planned-diffs list (chat) and writes `spec.yaml` + `planned-diffs.md` to
  `.ai/task-artifacts/CFG-001/`
- Agent waits for operator approval

2. Approval (operator)

- Operator reviews the chat spec and the working files (`.ai/task-artifacts/CFG-001/spec.yaml` and `planned-diffs.md`)
- Operator either requests changes or approves

3. On approval: branch & initial commit

- Agent creates branch per convention `<type>/<task-id>-<slug>` (e.g., `feat/CFG-001-add-config`)
- Agent updates `Tasks/CFG-001.yaml` status -> `in_progress` and adds an evidence entry (branch name and timestamp)
- Agent commits and pushes the updated task file as the FIRST commit on the new branch with message like
  `spec pass: branch created`

4. Scaffold pass (automated/interactive)

- The scaffold prompt reads the machine-readable `spec.yaml`
- Scaffold applies the minimal set of edits (scaffolding) listed in `planned_diffs` and commits them incrementally
  with descriptive messages
- Scaffold produces `scaffold-report.md` in the same `.ai/task-artifacts/CFG-001/` directory summarising applied diffs
  and any unresolved questions

5. Stabilize pass

- Run tests / linters / build
- Fix failures, iterate, and ensure acceptance criteria met
- Update `Tasks/CFG-001.yaml` (status -> `in_review`) and add evidence: commit SHAs, test summary, coverage report
  link (if CI), and a short note
- Commit the updated task file and any remaining fixes

6. Final review & merge

- Operator/Reviewer reviews the PR, verifies artifacts, and merges when satisfied.

Files created during the process (recommended):

- `.ai/task-artifacts/CFG-001/spec.yaml` (machine-readable spec)
- `.ai/task-artifacts/CFG-001/planned-diffs.md` (human-readable planned diffs and diff sketches)
- `.ai/task-artifacts/CFG-001/scaffold-report.md` (what scaffold applied)
- `.ai/task-artifacts/CFG-001/stabilize-report.md` (test results and final status)

Agent responsibilities (explicit):

- Never modify project files before the spec is approved and the task file is committed to the task branch as the first
  commit.
- Always write the spec artifact for scaffold to consume, unless the operator explicitly forbids it.
- Use the project's branch naming rules: `<type>/<task-id>-<slug>` and ensure branch name contains only one slash.
- Keep all artifacts under `.ai/task-artifacts/<TASK-ID>/` to make cleanup and auditing easy.

Edge cases & notes

- If the task acceptance criteria require secrets or credentials, agents must not write them to the repo: instead record
  a placeholder and a note instructing the operator how to supply secrets (e.g., via CI secret store).
- If planned diffs include large binary files or generated artifacts, prefer generating them in a build step rather than
  committing binaries.
- If a task touches many files, prefer batching commits by logical subtask with clear messages rather than one huge
  commit.

Next steps (for this session)

- If you agree with this approach, I'll update the spec-pass prompt to include an optional step to write the spec
  artifact (switchable via a boolean flag in the prompt YAML header, default `true`).
- I'll record your confirmation choice in these session notes and then we can draft the scaffold-pass prompt and its
  companion instructions.

---

## Update: scaffold-pass prompt and instructions added

- Added: `.github/prompts/002-scaffold-pass.md`
- Added: `.github/instructions/002-scaffold-pass-instructions.md`

Next steps:

- Review the scaffold-pass prompt and instructions. If approved, I'll draft the stabilize-pass prompt and instructions
  next.
- After creating stabilize, we'll run a quick dry run walkthrough of processing a sample task artifact to verify the
  end-to-end flow.

---

## Update: stabilize-pass prompt and instructions added

- Added: `.github/prompts/003-stabilize-pass.md`
- Added: `.github/instructions/003-stabilize-pass-instructions.md`

Next steps:

- Review the stabilize-pass prompt and instructions. If approved, I will run through a dry-run walkthrough using a
  sample `spec.yaml` to verify end-to-end behavior (spec -> scaffold -> stabilize).

---

Note: repository build/test guidance

- This repository may not build or run tests by design (it contains prompts, schemas, and docs). For the stabilize
  pass we will prefer running linters and static analysis where applicable and record results in the `stabilize.yaml`
  and `stabilize-report.md` artifacts.
- Details about running full build/test flows and coverage collection should be preserved here for use when creating
  per-template stabilize prompts (e.g., Java/Gradle, Node/npm, Python/pytest). These template-specific commands and
  checks will be added to the template prompts and recorded in these session notes to avoid losing them.

---

Note: commit message formatting (recurring)

- Do NOT embed literal `\n` in git commit messages. Use actual linefeeds either by:
  - multiple `-m` flags (each `-m` adds a new paragraph), or
  - providing a commit message file (`git commit -F message.txt`).
- This prevents messages from containing the characters `\n` instead of true newlines. This is a frequent source of
  review noise and must be avoided in examples and automation.
