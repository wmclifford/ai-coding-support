# ai-coding-support

Parent project for all things supporting use of AI coding agents

## What this repository provides

This meta-repository contains governance, templates, schemas, and examples for projects that will be bootstrapped
and maintained using AI coding agents. It is intentionally lightweight and intended to serve as a single source of
truth for best practices, agent prompts, and reusable CI/Action patterns.

## Quick start

1. Clone the repo:

   `git clone git@github.com:wmclifford/ai-coding-support.git`

2. Read the governance docs in `docs/governance/` to understand conventions, goals, and system-level rules.
3. Browse `templates/` for project starter templates (language-specific) and `examples/` for reference artifacts.

## Repository layout

- `docs/` — governance documents and guidance (source-of-truth for this meta-project)
- `examples/` — example governance and task files used as references
- `schemas/` — JSON/YAML schemas used by agents and validators
- `templates/` — project templates organized by language
- `.ai/` — agent session notes and drafts (working area; not for external consumption)
- `tools/` — small helper scripts and utilities

## Contributing

We follow the project's governance:

- Use Conventional Commits for commit messages.
- One task per PR; include `Refs: [TASK-ID]` in commit and PR footers.
- Follow the Two-commit Evidence ritual for tasks (CODE commit + EVIDENCE commit updating the task file).
- All changes to `docs/`, `templates/`, and `schemas/` must pass CI checks (format, gitleaks, schema validation).

If you're contributing, please open an issue or a task file under `examples/Tasks/` and follow the task lifecycle.

## Next steps

- Add a `templates/nodejs` bootstrap and a short CLI helper for project creation (planned).
- Add agent prompt templates under `templates/<language>/prompts`.

---
