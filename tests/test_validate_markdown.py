import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Set

# Import from tools directory by adjusting sys.path for tests
ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from validate_markdown import (  # type: ignore
    __version__,
    extract_h2_sections,
    parse_args,
    validate_markdown_file,
    validate_sections,
)


SAMPLE_MD = """
# Title

Some intro

## Overview
Content

### NotThis
More content

## Details
Some details

## Summary ####
Text

Normal text
""".strip()


class TestExtractH2Sections(unittest.TestCase):
    def test_extract_h2_sections_parses_only_h2(self):
        sections = extract_h2_sections(SAMPLE_MD)
        # Expect lower-cased normalized names
        self.assertSetEqual(sections, {"overview", "details", "summary"})

    def test_extract_h2_sections_trims_trailing_hashes_and_spaces(self):
        text = "## Heading ####   \nText"
        sections = extract_h2_sections(text)
        self.assertSetEqual(sections, {"heading"})


class TestValidateSections(unittest.TestCase):
    def test_validate_sections_missing_and_present(self):
        found = {"overview", "details"}
        expected = ["Overview", "Summary"]  # case-insensitive
        valid, missing = validate_sections(found, expected)
        self.assertFalse(valid)
        self.assertSetEqual(missing, {"summary"})

    def test_validate_sections_all_present(self):
        found = {"overview", "details", "summary"}
        expected = ["overview", "DETAILS"]  # case-insensitive
        valid, missing = validate_sections(found, expected)
        self.assertTrue(valid)
        self.assertSetEqual(missing, set())


class TestValidateMarkdownFile(unittest.TestCase):
    def test_missing_file_returns_false(self):
        valid, missing = validate_markdown_file("/path/does/not/exist.md", ["any"])
        self.assertFalse(valid)
        self.assertEqual(missing, {"any"})

    def test_valid_when_all_sections_present(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.md"
            p.write_text(SAMPLE_MD, encoding="utf-8")
            valid, missing = validate_markdown_file(p, ["overview", "summary"])  # case-insensitive
            self.assertTrue(valid)
            self.assertEqual(missing, set())

    def test_invalid_when_any_missing(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.md"
            p.write_text(SAMPLE_MD, encoding="utf-8")
            valid, missing = validate_markdown_file(p, ["overview", "bogus"])  # case-insensitive
            self.assertFalse(valid)
            self.assertEqual(missing, {"bogus"})


class TestParseArgs(unittest.TestCase):
    def test_parse_args_with_multiple_sections(self):
        ns = parse_args(["README.md", "-s", "Overview", "-s", "Details"])
        self.assertEqual(ns.markdown_file, "README.md")
        self.assertEqual(ns.sections, ["Overview", "Details"])

    def test_version_flag_exits(self):
        # argparse's version action raises SystemExit; ensure it's configured.
        with self.assertRaises(SystemExit) as ctx:
            parse_args(["--version"])  # missing required args, but --version exits before parse
        self.assertEqual(ctx.exception.code, 0)


class TestMainIntegration(unittest.TestCase):
    def run_cli(self, argv, text: str) -> int:
        from validate_markdown import main
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "file.md"
            p.write_text(text, encoding="utf-8")
            try:
                # Capture exit code without exiting interpreter
                return main([str(p)] + argv)
            except SystemExit as e:
                return int(e.code)

    def test_main_success_exit_code_zero(self):
        code = self.run_cli(["-s", "overview", "-s", "summary"], SAMPLE_MD)
        self.assertEqual(code, 0)

    def test_main_failure_when_missing_section(self):
        code = self.run_cli(["-s", "overview", "-s", "missing"], SAMPLE_MD)
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()

