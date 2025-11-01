# Coding Conventions

> Machine-readable summary

```yaml
project:
  name: ai-coding-support
  commit_header_case: "lower-case"
  commit_types: [ "feat","fix","docs","style","refactor","test","chore","perf","build","ci","revert" ]
  branch_naming: "<type>/<TASK-ID>-<slug>"
  prompt_templates_path: "templates/<language>/prompts"
  formatting_tools_by_stack:
    java: "spotless (Gradle) + prettier for MD/YAML"
    python: "black + isort + ruff"
    nodejs: "prettier + eslint"
    golang: "gofmt + golangci-lint"
  coverage_gate: 80
  agents_must_format_and_stage: true
```

## Code Structure

This repository is a "meta-project" that provides governance, templates, schemas, and example artifacts. Keep the
layout simple and discoverable so agents and humans can find templates and prompts quickly.

Recommended top-level layout (canonical):

```
/README.md                # repo-level quickstart and goals
/docs/                    # governance and project-level documentation
/examples/                # reference implementations and example projects
/schemas/                 # JSON/YAML schemas consumed by tooling and agents
/templates/               # project templates organized by language
  /<language>/
    /<template-name>/
      /prompts/           # prompt templates used by agents for this template
      /ci/                # example CI workflow snippets for the template
      README.md           # bootstrap instructions for the template
/.ai/                     # agent session logs and prompt drafts (private to repo)
/tools/                   # scripts and helper utilities (small, low-risk)

```

Guidelines:

- Templates must be self-contained: include a `README.md`, example tasks, prompt templates, and CI snippets where
  applicable.
- Keep example projects minimal (single-purpose) and focused on demonstrating governance, not full app features.
- Use `schemas/` to define machine-readable contracts that agents and CI will validate.

## Naming & Packaging

Naming should be predictable and follow the conventions of each target language, with a few cross-language
rules for artifacts produced by this repo.

Cross-language rules:

- Template directories: `templates/<language>/<template-name>` (kebab-case).
- Prompt files: `prompts/<role>.<format>` where `role` is one of `spec-author`, `implementer`, `reviewer` and
  `format` is `md` (human-readable) or `yaml`/`json` (machine-friendly). Examples:
  - `templates/nodejs/basic/prompts/spec-author.md`
  - `templates/java/springboot/prompts/implementer.yaml`
- Task files: use `examples/Tasks/<TASK-ID>.yaml` or `templates/<language>/<...>/tasks/<TASK-ID>.yaml` and ensure the
  filename contains the Task ID referenced in commits/PRs.
- CI snippets/workflows: place example workflows under `templates/<language>/<template-name>/ci/` and reference a
  canonical workflow in `docs/`.

Language-specific guidance (examples):

- Node.js: package name and NPM scope should be lower-case kebab-case; entry point `index.js`/`index.mjs` or as
  specified in `package.json`.
- Java: groupId/org packages follow reverse-domain style (e.g., `io.github.<owner>.<project>`). Use Gradle with
  clear module names mirroring template naming.
- Python: packages are lower_case_with_underscores; prefer a top-level package matching the template name.
- Go: module path should be the canonical VCS path (e.g., `github.com/<owner>/<repo>`), packages short and focused.

Packaging notes:

- Keep templates small; do not vendor heavy dependencies into templates. Use CI to validate dependency installation.
- Document `bootstrap` steps clearly in the template's README and include example commands for agents to run.

## Documentation

- Keep README up to date.

## Formatting

- Source of truth: `.editorconfig`
- Enforced via: `eslint`, `prettier` (for Node), `spotless` (for Java), `black`/`ruff` (for Python), `gofmt`/
  `golangci-lint` (for Go)
- Auto-fixable via: `eslint --fix`, `spotlessApply`, `black --fast --quiet`
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

- Scope guidance: use scope to indicate the slice/component of the repository you changed (e.g., `docs`, `ci`,
  `governance`, `schemas`, `templates/java`, `examples`). Do NOT use the Task ID as scope; reference the Task ID in the
  commit footer using `Refs: <TASK-ID>`.

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
- `perf`: performance improvements
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

Note: The task file schema supports optional `evidence.timestamp` (ISO-8601) and `evidence.branchName` (the branch used
for the task). Populate these where helpful.

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
