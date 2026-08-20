#!/usr/bin/env python3
"""Tests for the AI Project OS whitebox scanner."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("whitebox_scan.py")
SPEC = importlib.util.spec_from_file_location("whitebox_scan", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("Cannot load whitebox_scan.py")
whitebox_scan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(whitebox_scan)


class WhiteboxScanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.placeholder_value = "-".join(["placeholder", "secret", "value"])
        self.actual_value = "-".join(["actual", "super", "secret"])
        self.ignored_marker = "-".join(["ignored", "secret", "marker"])
        self.dependency_version = "-".join(["not", "emitted", "version"])
        self._write(".gitignore", "node_modules/\n")
        self._write(
            "package.json",
            json.dumps(
                {
                    "dependencies": {"react": self.dependency_version},
                    "devDependencies": {"vitest": self.dependency_version},
                }
            ),
        )
        self._write("src/main.py", "print('fixture')\n")
        self._write("tests/test_app.py", "def test_fixture():\n    assert True\n")
        self._write("docs/README.md", "# Fixture\n")
        self._write("migrations/001_create.sql", "create table example(id int);\n")
        self._write(
            ".env.example",
            f"API_TOKEN={self.placeholder_value}\nPUBLIC_MODE=true\n",
        )
        self._write(".env", f"PASSWORD={self.actual_value}\n")
        self._write("node_modules/ignored.js", f"{self.ignored_marker}\n")
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @property
    def output_dir(self) -> Path:
        return self.root / "project-os" / "discovery"

    def test_dry_run_is_read_only_and_ignored_paths_stay_excluded(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), "--summary"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.output_dir / whitebox_scan.OUTPUT_NAME).exists())

        evidence = whitebox_scan.build_evidence(self.root, self.output_dir)
        rendered = whitebox_scan.render_json(evidence)
        self.assertNotIn("node_modules/ignored.js", rendered)
        self.assertNotIn(self.ignored_marker, rendered)

    def test_names_are_collected_without_secret_or_setting_values(self) -> None:
        evidence = whitebox_scan.build_evidence(self.root, self.output_dir)
        rendered = whitebox_scan.render_json(evidence)

        self.assertIn('"key": "API_TOKEN"', rendered)
        self.assertIn('"key": "PUBLIC_MODE"', rendered)
        self.assertIn('"name": "react"', rendered)
        self.assertIn('"name": "vitest"', rendered)
        self.assertIn('".env"', rendered)
        self.assertNotIn(self.placeholder_value, rendered)
        self.assertNotIn(self.actual_value, rendered)
        self.assertNotIn(self.dependency_version, rendered)

    def test_write_is_deterministic_and_check_passes(self) -> None:
        first = whitebox_scan.render_json(
            whitebox_scan.build_evidence(self.root, self.output_dir)
        )
        written = whitebox_scan.write_evidence(self.output_dir, first)
        second = whitebox_scan.render_json(
            whitebox_scan.build_evidence(self.root, self.output_dir)
        )
        self.assertEqual(first, second)
        self.assertEqual(written.read_text(encoding="utf-8"), second)

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), "--check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[PASS]", result.stdout)

    def test_output_directory_cannot_escape_repository(self) -> None:
        with self.assertRaises(whitebox_scan.ScanError):
            whitebox_scan.resolve_output_dir(self.root, "../outside")


if __name__ == "__main__":
    unittest.main()
