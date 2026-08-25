#!/usr/bin/env python3
"""Tests for guarded AI Project OS upgrade discovery, planning, and apply."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).with_name("upgrade_project_os.py")
SPEC = importlib.util.spec_from_file_location("upgrade_project_os", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("Cannot load upgrade_project_os.py")
upgrade = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = upgrade
SPEC.loader.exec_module(upgrade)


def version_file(version: str, installed_date: str, customization: str) -> str:
    return f"""# OS_VERSION

```text
Product: AI Project OS
Installed OS Version: {version}
Installed Date: {installed_date}
Local Customizations: {customization}
Last Upgrade: fixture
```

## Compatibility

Fixture compatibility.
"""


class UpgradeProjectOSTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.installed = self.root / "project-os"
        self.base = self.root / "base" / "project-os"
        self.target = self.root / "target" / "project-os"
        for path in [self.installed, self.base, self.target]:
            (path / "audit").mkdir(parents=True)
            (path / "OS_VERSION.md").write_text(
                version_file(
                    "v0.6.0" if path != self.target else "v0.8.0",
                    "2026-01-01" if path != self.installed else "2025-12-31",
                    "template" if path != self.installed else "keep my local policy",
                ),
                encoding="utf-8",
            )
            (path / "RULES.md").write_text(
                "base rules\n" if path != self.target else "target rules\n",
                encoding="utf-8",
            )
            (path / "LOCAL_ONLY.md").write_text("base local\n", encoding="utf-8")
            (path / "audit" / "HISTORY.md").write_text(
                "project history\n" if path == self.installed else "template history\n",
                encoding="utf-8",
            )
        (self.installed / "LOCAL_ONLY.md").write_text("my local change\n", encoding="utf-8")
        (self.installed / "ORPHAN.md").write_text("installed only\n", encoding="utf-8")
        (self.target / "NEW.md").write_text("new target file\n", encoding="utf-8")
        (self.root / "README.md").write_text("fixture repo\n", encoding="utf-8")
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "fixture"], cwd=self.root, check=True)
        subprocess.run(["git", "switch", "-qc", "codex/upgrade-fixture"], cwd=self.root, check=True)

    def tearDown(self) -> None:
        os.environ.pop("AIPOS_OS_UPGRADE_APPROVED", None)
        self.temp_dir.cleanup()

    def config(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "installed_path": "project-os",
            "source": {"type": "directory", "path": "target/project-os"},
            "base": {"type": "directory", "path": "base/project-os"},
            "allow_downgrade": False,
            "as_of": "2026-08-25T12:00:00Z",
            "protected_paths": [],
            "apply_policy": {
                "max_plan_age_minutes": 60,
                "authorization_env": "AIPOS_OS_UPGRADE_APPROVED",
                "branch_prefix": "codex/upgrade-",
            },
        }

    def action_map(self, plan: dict[str, object]) -> dict[str, dict[str, object]]:
        return {item["path"]: item for item in plan["actions"]}

    def test_inspection_compares_semantic_versions_without_writes(self) -> None:
        result = upgrade.inspect_upgrade(self.config(), self.root)
        self.assertEqual("v0.6.0", result["installed_version"])
        self.assertEqual("v0.8.0", result["available_version"])
        self.assertEqual("upgrade", result["relation"])
        self.assertEqual([], result["blockers"])

    def test_downgrade_fails_closed_without_explicit_policy(self) -> None:
        (self.target / "OS_VERSION.md").write_text(
            version_file("v0.5.0", "2026-01-01", "template"), encoding="utf-8"
        )
        result = upgrade.inspect_upgrade(self.config(), self.root)
        self.assertEqual("downgrade", result["relation"])
        self.assertTrue(result["blockers"])

    def test_three_way_plan_classifies_and_protects_project_memory(self) -> None:
        plan = upgrade.build_plan(self.config(), self.root)
        actions = self.action_map(plan)
        self.assertEqual("READY", plan["status"])
        self.assertEqual("migrate", actions["OS_VERSION.md"]["action"])
        self.assertEqual("safe_update", actions["RULES.md"]["action"])
        self.assertEqual("preserve", actions["LOCAL_ONLY.md"]["action"])
        self.assertEqual("preserve", actions["audit/HISTORY.md"]["action"])
        self.assertTrue(actions["audit/HISTORY.md"]["protected"])
        self.assertEqual("add", actions["NEW.md"]["action"])
        self.assertEqual("remove_candidate", actions["ORPHAN.md"]["action"])
        self.assertEqual(plan["plan_id"], upgrade.build_plan(self.config(), self.root)["plan_id"])

    def test_both_modified_file_blocks_apply(self) -> None:
        (self.installed / "RULES.md").write_text("local rules\n", encoding="utf-8")
        plan = upgrade.build_plan(self.config(), self.root)
        self.assertEqual("BLOCKED", plan["status"])
        self.assertEqual("conflict", self.action_map(plan)["RULES.md"]["action"])
        self.assertTrue(any("RULES.md" in item for item in plan["blockers"]))

    def test_plan_contains_hashes_not_file_content(self) -> None:
        secret_marker = "PRIVATE-CONTEXT-MUST-NOT-APPEAR"
        (self.installed / "audit" / "HISTORY.md").write_text(secret_marker, encoding="utf-8")
        plan = upgrade.build_plan(self.config(), self.root)
        rendered = json.dumps(plan, sort_keys=True)
        self.assertNotIn(secret_marker, rendered)
        self.assertIn("installed_sha256", rendered)

    def test_apply_requires_cli_runtime_branch_and_freshness_gates(self) -> None:
        plan = upgrade.build_plan(self.config(), self.root)
        with self.assertRaises(upgrade.UpgradeError):
            upgrade.apply_plan(plan, self.root, False, "2026-08-25T12:01:00Z")
        os.environ["AIPOS_OS_UPGRADE_APPROVED"] = "APPROVED"
        with self.assertRaises(upgrade.UpgradeError):
            upgrade.apply_plan(plan, self.root, True, "2026-08-25T14:00:00Z")
        subprocess.run(["git", "switch", "-qc", "codex/not-upgrade"], cwd=self.root, check=True)
        with self.assertRaises(upgrade.UpgradeError):
            upgrade.apply_plan(plan, self.root, True, "2026-08-25T12:01:00Z")

    def test_apply_preserves_memory_and_is_idempotent(self) -> None:
        plan = upgrade.build_plan(self.config(), self.root)
        original_audit = (self.installed / "audit" / "HISTORY.md").read_bytes()
        original_local = (self.installed / "LOCAL_ONLY.md").read_bytes()
        os.environ["AIPOS_OS_UPGRADE_APPROVED"] = "APPROVED"
        first = upgrade.apply_plan(plan, self.root, True, "2026-08-25T12:01:00Z")
        second = upgrade.apply_plan(plan, self.root, True, "2026-08-25T12:02:00Z")
        self.assertEqual("target rules\n", (self.installed / "RULES.md").read_text(encoding="utf-8"))
        self.assertEqual("new target file\n", (self.installed / "NEW.md").read_text(encoding="utf-8"))
        self.assertEqual(original_audit, (self.installed / "audit" / "HISTORY.md").read_bytes())
        self.assertEqual(original_local, (self.installed / "LOCAL_ONLY.md").read_bytes())
        version = (self.installed / "OS_VERSION.md").read_text(encoding="utf-8")
        self.assertIn("Installed OS Version: v0.8.0", version)
        self.assertIn("Local Customizations: keep my local policy", version)
        self.assertTrue(any(item["status"] == "applied" for item in first["actions"]))
        self.assertTrue(any(item["status"] == "already_applied" for item in second["actions"]))
        verification, code = upgrade.verify_plan(plan, self.root)
        self.assertEqual(0, code)
        self.assertEqual("pass", verification["status"])

    def test_unrelated_tracked_change_blocks_apply(self) -> None:
        plan = upgrade.build_plan(self.config(), self.root)
        os.environ["AIPOS_OS_UPGRADE_APPROVED"] = "APPROVED"
        (self.root / "README.md").write_text("unrelated change\n", encoding="utf-8")
        with self.assertRaises(upgrade.UpgradeError):
            upgrade.apply_plan(plan, self.root, True, "2026-08-25T12:01:00Z")

    def test_zip_path_traversal_is_rejected(self) -> None:
        archive = self.root / "unsafe.zip"
        with zipfile.ZipFile(archive, "w") as bundle:
            bundle.writestr("project-os/OS_VERSION.md", version_file("v0.8.0", "x", "x"))
            bundle.writestr("project-os/../escape.txt", "escape")
        with self.assertRaises(upgrade.UpgradeError):
            upgrade.load_zip_tree(archive)


if __name__ == "__main__":
    unittest.main()
