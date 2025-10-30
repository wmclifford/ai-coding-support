# Coding Conventions

## Code Structure

## Naming & Packaging

## Documentation

- Keep README up to date.

## Formatting

- Source of truth: `.editorconfig`
- Enforced via: `eslint`, `prettier`
- Auto-fixable via: `eslint --fix`
- Auto-format via: `prettier --write`
- Agents must run formatting after edits and re-stage only formatted files.

## Commits & Branches

### Conventional Commits

See [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for full documentation.

**Format:**

```markdown
<type>(<optional scope>): <description>

[optional body]

Refs: [<TASK-ID>]
```

**Body:**

- Use the imperative, present tense: "change" not "changed" nor "changes"
- Use bullet points for the body
- Wrap lines at 100 characters
- When only changing documentation, include `[ci skip]` in the commit body on its own line

**Types:**

- `feat`: new feature
- `fix`: bug fix
- `docs`: documentation
- `style`: formatting, missing semicolons, etc.; no code change
- `refactor`: refactoring production code
- `test`: adding tests, refactoring test; no production code change
- `chore`: updating build tasks, package manager configs, etc; no production code change
- `revert`: reverting a previous commit
- `build`: changes that affect the build system or external dependencies
- `ci`: changes to our CI configuration files and scripts

**Miscellaneous:**

- `BREAKING CHANGE:` in the commit body, when the commit introduces a breaking change
- [TASK-ID]: the category ID, e.g. `[PAG-002]`
- Use `!` after scope to mark breaking change, per spec: `feat(api)!: ...`
- Use actual line feeds when generating commit messages; do not use `\n` in the message. This is
  important when using `git commit -m` to generate a commit message.

### Two-commit Evidence Ritual

1. CODE commit implements the task.
2. EVIDENCE commit updates the task file (`Tasks/<TASK-ID>.yaml`) with `evidence.commit` = 40-char commit hash.

### Additional Rules

- **One task per PR** preferred; avoid mixing concerns.
- **Branch Naming:** `<type>/<TASK-ID>-<slug>`; e.g. `feat/PAD-002-add-new-feature`
- Agents must create/checkout branch after spec approval and before edits; task file status must be
  updated to `in_progress`, and the task file must be committed to the branch before any code changes.
- Merging:
    - Local: linear history per task (rebase or squash locally).
    - Remote: **squash merges** recommended; PR title must follow Conventional Commits format.

## Task Lifecycle (cheat sheet)

```markdown
`pending` (task file created and exists on `main` branch)
-> `in_progress` (branch created)
-> `in_review` (branch pushed, PR created)
-> `done` (PR merged and evidence commit present)
```

- **`pending`:** task file exists on `main` branch; task is not yet started.
- **`in_progress`:** should be updated as first commit when branch is created, before any code changes.
- **`in_review`:** task file must be updated with `evidence.commit` = <code SHA> and status set to `in_review` as
  last commit on the branch, just before PR is opened.
- **`done`:** task branch has been merged to `main`; the task file must be updated with `status` = `done` and
  the `evidence.commit` must be updated to the squash commit of the PR; commit this directly to `main`.

## Templates

- Commit message template: `docs/commits/.gitmessage`
- Pull request template: `.github/pull_request_template.md`
- Task files must follow the schema defined in `schemas/task-file.schema.v0.1.json`

The `templates` directory contains templates for various types of projects, providing a starting point for
new projects. These will be added to as the project evolves.

## Build & CI

- Lint rules auto-fix where possible; remaining violations block PR.

## Deviations

- Any deviation must include a short ADR entry with rationale and consequences.
