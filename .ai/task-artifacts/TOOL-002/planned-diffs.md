# Planned Diffs for TOOL-002

This plan introduces a YAML validation CLI tool and documentation.

## Branch

- Name: feat/TOOL-002-validate-yaml
- First commit will update `Tasks/TOOL-002.yaml` to `in_progress` and add spec artifacts.

## Changes

1) Add `tools/validate_yaml.py`
  - New Python 3 script implementing:
    - argparse CLI: `validate_yaml.py <yaml_file> <schema_file>` plus `--help` and `--version` (0.1.0)
    - Functions: parse_args, read_yaml, read_json, validate_instance, format_errors, validate_yaml_against_schema, main
    - Uses jsonschema.Draft202012Validator.iter_errors and yaml.safe_load
    - Logging configured with logging.basicConfig()
  - Behavior:
    - Exit 0 and print 'OK' when valid
    - Exit 1 and print list of errors otherwise

2) Add `tests/test_validate_yaml.py`
  - Unit tests for each function, including CLI integration tests.
  - Temporary files for valid/invalid YAML against a simple Draft 2020-12 schema.

3) Add `requirements.txt`
  - Add:
    - jsonschema
    - PyYAML

4) Update `tools/README.md`
  - Ensure alphabetical order by filename.
  - Add/ensure the following H2 sections:
    - `## validate_markdown.py`: short purpose and usage example.
    - `## validate_yaml.py`: purpose, usage, and links to documentation for jsonschema and PyYAML.

## Justification

- Meets acceptance criteria and provides a reusable validation tool used by the agent.
- Tests ensure reliability and provide examples for future contributors.

