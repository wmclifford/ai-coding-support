import json
import tempfile
import unittest
from pathlib import Path

# Ensure tools directory is importable
import sys
ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from validate_yaml import (  # type: ignore
    __version__,
    format_errors,
    main,
    parse_args,
    read_json,
    read_yaml,
    validate_instance,
    validate_yaml_against_schema,
)


class TestParseArgs(unittest.TestCase):
    def test_parse_args_positional(self):
        ns = parse_args(["file.yaml", "schema.json"])
        self.assertEqual(ns.yaml_file, "file.yaml")
        self.assertEqual(ns.schema_file, "schema.json")

    def test_version_flag_exits(self):
        with self.assertRaises(SystemExit) as ctx:
            parse_args(["--version"])  # exits early
        self.assertEqual(ctx.exception.code, 0)


class TestIO(unittest.TestCase):
    def test_read_yaml_success_and_failure(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ok.yaml"
            p.write_text("a: 1\n", encoding="utf-8")
            data = read_yaml(p)
            self.assertEqual(data, {"a": 1})
            # invalid YAML
            q = Path(td) / "bad.yaml"
            q.write_text("a: [1, 2", encoding="utf-8")  # missing closing ]
            with self.assertRaises(Exception):
                read_yaml(q)

    def test_read_json_success_and_failure(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "ok.json"
            p.write_text(json.dumps({"type": "object"}), encoding="utf-8")
            data = read_json(p)
            self.assertEqual(data, {"type": "object"})
            q = Path(td) / "bad.json"
            q.write_text("{\n", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                read_json(q)


class TestValidation(unittest.TestCase):
    def schema(self):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["name", "age"],
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer", "minimum": 0},
            },
            "additionalProperties": False,
        }

    def test_validate_instance_valid_and_invalid(self):
        s = self.schema()
        valid, errs = validate_instance({"name": "a", "age": 1}, s)
        self.assertTrue(valid)
        self.assertEqual(errs, [])
        valid, errs = validate_instance({"name": 1, "age": -1}, s)
        self.assertFalse(valid)
        self.assertGreaterEqual(len(errs), 1)

    def test_format_errors_sorts_and_formats(self):
        s = self.schema()
        _, errs = validate_instance({"name": 1, "age": -1}, s)
        lines = format_errors(errs)
        self.assertTrue(any("name" in ln or "age" in ln for ln in lines))


class TestIntegration(unittest.TestCase):
    def test_validate_yaml_against_schema_ok_and_fail(self):
        with tempfile.TemporaryDirectory() as td:
            yaml_ok = Path(td) / "data.yaml"
            yaml_bad = Path(td) / "bad.yaml"
            schema = Path(td) / "schema.json"
            yaml_ok.write_text("name: Jane\nage: 30\n", encoding="utf-8")
            yaml_bad.write_text("name: 5\n", encoding="utf-8")
            schema.write_text(json.dumps({
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "additionalProperties": False
            }), encoding="utf-8")

            ok, errors = validate_yaml_against_schema(yaml_ok, schema)
            self.assertTrue(ok)
            self.assertEqual(errors, [])

            ok, errors = validate_yaml_against_schema(yaml_bad, schema)
            self.assertFalse(ok)
            self.assertGreater(len(errors), 0)

    def test_main_exit_codes(self):
        with tempfile.TemporaryDirectory() as td:
            data = Path(td) / "d.yaml"
            schema = Path(td) / "s.json"
            data.write_text("name: Jane\nage: 22\n", encoding="utf-8")
            schema.write_text(json.dumps({
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "additionalProperties": False
            }), encoding="utf-8")

            # Should exit 0
            code = main([str(data), str(schema)])
            self.assertEqual(code, 0)

            # Make invalid
            data.write_text("name: 1\n", encoding="utf-8")
            code = main([str(data), str(schema)])
            self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
