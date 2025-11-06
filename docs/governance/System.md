# System-Level Instructions

> Machine-readable summary

```yaml
project:
  name: ai-coding-support
  ci_checks:
    - commitlint
    - markdownlint
    - prettier
    - gitleaks
    - schema_validation
    - linkcheck
  secrets_scan: true
  releases: semantic-release
  task_validator_repo: "<TOOLING_REPO_PLACEHOLDER>" # replace with actual tooling repo URL when available
  publish_actions_from_repo: true
  branch_policy: "trunk-based (squash merges, PR required, commitlint titles)"
  approval_model: "owner-driven"
```

## Security

- **Never** store secrets in source code, configuration files, or documentation; use repository secrets instead.
- Use short-lived tokens and least privilege for automation. For publishing or automation that requires long-lived
  credentials, store them in an organization-level secrets store and rotate regularly.
- Protect sensitive branches (`main`) with branch protection rules: require PRs, require passing status checks, require
  reviews, and limit who can push directly.
- Audit access to repository secrets and review secret usage periodically.

## CI/CD

This repository is a meta-repo and does not produce build artifacts. CI workflows focus on validation, linting,
security scanning, and publishing of repo-level artifacts (templates, actions, docs).

Recommended CI job matrix (example roles):

- commitlint: validate commit messages on push/PR.
- markdownlint: lint docs and templates (fail on serious issues).
- prettier/check-format: ensure formatting of code/markdown/YAML.
- gitleaks: secrets scan focused on changed files (templates, docs, workflows).
- schema-validation: validate `examples/Tasks` and any `templates/*/tasks` against `schemas/task-file.schema.v0.1.json`.
  - Implementation note: the schema validator is expected to live in an external tooling repo; example workflow should
    call the validator from that repo (CLI container or action) and fail the job on validation errors.
- linkcheck/site: optional link checking for docs and example READMEs.
- publish-actions: runs only on releases or tagged commits; handles packaging/publishing of reusable GitHub Actions or
  composite actions. Requires a `GH_TOKEN` (or similar) stored as a repo/organization secret and least-privilege token
  usage.

CI behavior and gating:

- PRs that change governance, templates, schemas, or `.github/workflows` must pass all checks listed above.
- Block merges on any failure by using branch protection rules.
- For speed, run fast checks (commitlint, quick lint) early; run heavier checks (schema validation, full gitleaks) in a
  subsequent job or in a PR `check` job.

Example workflow guidance (do not add the workflow file here; add to `.github/workflows/ci.yml` as an example):

- Use matrix jobs to parallelize format/lint/security checks.
- Use an input parameter or environment variable to point to the `TOOLING_REPO` for schema validation (keep default as a
  placeholder until tooling repo exists).

## Branch & Merge Policy

- PR is **required** to merge to `main`.
- **Trunk-based** development:
  - require squash merges to `main`.
  - PR title must be a Conventional Commit.
  - include `Refs: [TASK-ID]` in the PR footer.
- CI **must** pass before merging.
- Code review is required; **at least 1 approving review** — may be manual or assisted by an AI reviewer.
- Consider required reviewers for sensitive changes (templates, workflows, schemas).

## Evidence & Audit

- Completed tasks must have `evidence.commit` set to the code SHA present in the repository:
  - Before the PR is merged, this will be the SHA of the PR branch commit referenced in the task file.
  - After the PR is merged, this will be the SHA of the squashed commit on the `main` branch.
- `evidence.prUrl` should reference the PR URL for the audit trail.
- `evidence.ciRunUrl` may remain empty for this repo (it does not build artifacts), but templates that include CI should
  prefer linking to the CI run for traceability.
- Keep an audit trail in tasks and record the `evidence.commit` and `evidence.prUrl` for all tasks (documentation,
  examples, and production tasks) per the agreed evidence policy.

## Releases & Publishing

- Use `semantic-release` (or similar) for automatic changelog and release tagging where appropriate for templates or
  actions published from this repo.
- Publishing reusable GitHub Actions from this repo:
  - Store action definitions under `.github/actions/<action-name>` or a top-level `actions/` directory.
  - Use version tags and `semantic-release` to publish tags and update `action.yml` references accordingly.
  - Publishing requires a repo token with `contents: write` and `packages: write` where applicable; prefer short-lived
    deploy tokens and store them as repository/organization secrets.
- If action publishing grows beyond a small set (5–10), consider moving heavy-weight actions to dedicated repositories
  and
  keep small composite actions here.

## Validation tooling (external)

- The task-file validator and other enforcement tooling are expected to live in a separate tooling repo (see
  `task_validator_repo` placeholder in the YAML header). Example validators:
  - Task schema validation (JSON/YAML schema check); presently supported by `tools/validate_yaml.py`.
  - Task status and evidence checks (ensures `evidence.commit` present when required).
  - Documentation link and build checks.

- Example invocation from a workflow: call a Dockerized CLI from the tooling repo or call a published GitHub Action that
  runs the validator. The example workflow should fail the job when validation fails.

## Secrets & Credentials

- Store tokens in repository or organization secrets (GitHub Actions secrets). Do not print secrets in logs. Use
  `ACTIONS_STEP_DEBUG` carefully and avoid revealing secrets.
- Prefer scoped tokens (repo-level or fine-grained tokens) and rotate them regularly.
- For publishing actions/releases, use a separate deploy token with limited scope and store it as a repo secret.
- If using third-party CI or external runners, ensure secrets are provisioned via secure vaults and audited.

## Observability & Monitoring

- This repo publishes docs and templates; include basic monitoring via CI job success/failure notifications (Slack,
  email) as part of downstream projects that consume the templates.
- Encourage template consumers to add health and observability guidance in their template READMEs.

## Deviations & ADRs

- Any deviation from these system-level rules must be recorded as an ADR in `docs/governance/ADR.md` with rationale,
  rollback plan, and approval signature (owner-driven by default).
