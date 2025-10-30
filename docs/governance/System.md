# System-Level Instructions

## Security

- **Never** store secrets in source code, configuration files, or documentation; use repository secrets instead.

## CI/CD

- Static analysis: secrets scan via `gitleaks`.
- PR checks: `commitlint`, `markdownlint`, `prettier`, `gitleaks`.
- Releases: `semantic-release`.
- Validation scripts: **optional** task status validator script (fails PR if task JSON has an invalid status or is
  missing evidence). Validation tools run on PRs and on release; will be added as they become available.
- Block merge on any failure.

## Branch & Merge Policy

- PR is **required** to merge to `main`.
- **Trunk-based** development:
    - require squash merges to `main`.
    - PR title must be a Conventional Commit.
    - include `Refs: [TASK-ID]` in the PR footer.
- Every PR references a **Task ID** in the footer (same [TASK-ID] as in commits).
- CI **must** pass.
- Code review is required; **at least 1 approving review** - may be manual, use Copilot, or both.

## Evidence & Audit

- Completed tasks must have `evidence.commit` set to the code SHA present in the repository:
    - Before the PR is merged, this will be the SHA of the PR branch.
    - After the PR is merged, this will be the SHA of the squashed commit on the `main` branch.
- `evidence.prUrl` should reference the PR URL for audit trail.
- `evidence.ciRunUrl` should remain empty as this project does not build anything.
