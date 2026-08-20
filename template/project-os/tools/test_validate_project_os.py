#!/usr/bin/env python3
"""Tests for source-repository and installed-package validator layouts."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


class ValidateProjectOsTests(unittest.TestCase):
    def test_current_layout_passes_strict_validation(self) -> None:
        project_os = Path(__file__).resolve().parents[1]
        root = project_os.parent
        validator = project_os / "tools" / "validate_project_os.py"

        result = subprocess.run(
            [sys.executable, str(validator), "--root", str(root), "--strict"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 failure(s), 0 warning(s)", result.stdout)


if __name__ == "__main__":
    unittest.main()
