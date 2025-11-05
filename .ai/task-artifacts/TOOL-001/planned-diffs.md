# Planned Diffs for TOOL-001 — Validate Markdown (Spec Pass)

Summary: Add a small Python CLI tool that validates a Markdown file exists and contains all required level-two
headings (## <SECTION>), plus unit tests. No external dependencies.

## Branch Plan

- Name: feat/TOOL-001-validate-markdown
- First commit content (after approval):
  - Update `Tasks/TOOL-001.yaml` status to `in_progress` and (optionally) populate evidence fields (branchName,
    timestamp)
  - Add `.ai/task-artifacts/TOOL-001/spec.yaml` and this `planned-diffs.md`
- First commit message:
  - Subject: chore(artifacts): start task branch and add spec artifacts
  - Footer: Refs: TOOL-001

## Changes

1) CREATE tools/validate_markdown.py

- Purpose: CLI to validate existence and required H2 sections.
- Key elements:
  - Version: 0.1.0
  - logging.basicConfig(level=INFO) and module-level logger
  - Functions:
    - parse_args(args): builds argparse parser; positional `markdown_file`; repeated `-s/--section` (at least one
      required); --version
    - read_text(path): returns file contents as str; raises FileNotFoundError if missing
    - extract_h2_sections(markdown_text): returns a set of H2 headings, stripping trailing `#` and whitespace
    - validate_sections(found_sections, expected_sections): returns tuple(valid: bool, missing: set[str])
    - validate_markdown_file(path, expected_sections): True if file exists and all expected are present; False otherwise
    - main(): wires everything; exit code 0 on success, 1 on failure; prints missing sections summary when invalid
- I/O and behavior:
  - Case-insensitive match on section names (trimmed); normalize both found and expected names to lower-case when
    comparing.
  - Ignores heading levels other than H2.
  - No external libs.

2) CREATE tests/test_validate_markdown.py

- Purpose: unittest coverage for each function and main behavior.
- Test cases:
  - extract_h2_sections: parses typical headings; ignores #, ###; trims trailing hashes/spaces
  - validate_sections: returns missing set correctly; valid when empty
  - validate_markdown_file:
    - returns False when file does not exist
    - returns True when all expected sections present
    - returns False when any expected missing
  - parse_args: parses positional file and multiple -s/--section values; --version prints version and exits
  - main/exit codes: using patch of sys.argv, ensure 0 for valid, 1 for invalid
  - case-insensitive behavior: expected sections match regardless of case differences in file vs input

## Justification

- Matches acceptance criteria in `Tasks/TOOL-001.yaml` (CLI, argparse, unittest, stdlib, logging, functions + main, H2
  validation rule) and user preference for case-insensitive section matching.
- Low-risk, self-contained; placed under `tools/` and `tests/` per repo conventions.

## Notes / Open Questions

- Alternative CLI: could accept sections as trailing positional args; we chose repeated -s/--section to be explicit and
  common.
