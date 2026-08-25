#!/usr/bin/env python3
"""Tests for deterministic AI Project OS release packaging."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("build_release.py")
SPEC = importlib.util.spec_from_file_location("build_release", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("Cannot load build_release.py")
build_release = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = build_release
SPEC.loader.exec_module(build_release)


class BuildReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        source = self.root / "template" / "project-os"
        (source / "tools").mkdir(parents=True)
        (source / "START_HERE.md").write_text("start\n", encoding="utf-8")
        tool = source / "tools" / "runner.py"
        tool.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        tool.chmod(0o755)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "fixture@example.invalid"],
            cwd=self.root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture"], cwd=self.root, check=True
        )
        subprocess.run(["git", "add", "template"], cwd=self.root, check=True)
        subprocess.run(
            ["git", "commit", "-qm", "fixture"], cwd=self.root, check=True
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_build_is_byte_deterministic_with_fixed_metadata(self) -> None:
        first = build_release.build_release(self.root, "releases/first.zip")
        second = build_release.build_release(self.root, "releases/second.zip")
        first_path = self.root / str(first["output"])
        second_path = self.root / str(second["output"])
        self.assertEqual(first_path.read_bytes(), second_path.read_bytes())
        self.assertEqual(first["sha256"], second["sha256"])
        with zipfile.ZipFile(first_path) as archive:
            names = archive.namelist()
            self.assertIn("project-os/START_HERE.md", names)
            self.assertNotIn("template/project-os/START_HERE.md", names)
            for info in archive.infolist():
                self.assertEqual(build_release.FIXED_ZIP_TIME, info.date_time)

    def test_build_rejects_dirty_source_and_output_escape(self) -> None:
        dirty = self.root / "template" / "project-os" / "uncommitted.md"
        dirty.write_text("not committed\n", encoding="utf-8")
        with self.assertRaises(build_release.BuildError):
            build_release.build_release(self.root, "releases/dirty.zip")
        dirty.unlink()
        with self.assertRaises(build_release.BuildError):
            build_release.build_release(self.root, "outside.zip")


if __name__ == "__main__":
    unittest.main()
