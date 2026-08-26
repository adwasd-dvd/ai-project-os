#!/usr/bin/env python3
"""Tests for the AI Project OS v1.0 rescue orchestrator."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("rescue_project.py")
SPEC = importlib.util.spec_from_file_location("rescue_project", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("Cannot load rescue_project.py")
rescue_project = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rescue_project)


class RescueProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self._write("package.json", json.dumps({"dependencies": {"demo-lib": "1.0.0"}}))
        self._write("package-lock.json", "{}\n")
        self._write("src/main.py", "print('fixture')\n")
        self._write("tests/test_app.py", "def test_fixture():\n    assert True\n")
        self._write("README.md", "# Mature Fixture\n")
        self._write(".github/workflows/test.yml", "name: test\n")
        self._write("project-os/ignored-os-doc.md", "# Installed OS\n")
        self._write_input()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture"], check=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _write(self, relative: str, content: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    @property
    def input_path(self) -> Path:
        return self.root / "project-os" / "rescue" / "RESCUE_INPUT.json"

    @property
    def output_dir(self) -> Path:
        return self.root / "project-os" / "rescue"

    def _input(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "project": {
                "name": "Mature Fixture",
                "target_version": "v1.0.0",
                "feature_prefix": "FIXTURE",
                "language": "en+zh",
                "exclude_prefixes": ["project-os"],
            },
            "linear": {
                "project": "Mature Fixture",
                "milestone": "v1.0.0",
                "write_approved": False,
            },
            "human_gates": {
                "baseline_confirmed": True,
                "decisions_resolved": True,
                "uat_passed": False,
            },
            "findings": [],
            "resolutions": [],
        }

    def _write_input(self, value: dict[str, object] | None = None) -> None:
        self._write(
            "project-os/rescue/RESCUE_INPUT.json",
            json.dumps(value or self._input(), ensure_ascii=False, indent=2) + "\n",
        )

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_inspect_is_read_only_and_excludes_installed_os(self) -> None:
        result = self._run(
            "inspect", "--input", "project-os/rescue/RESCUE_INPUT.json", "--summary"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Evidence written / 已写证据: No / 否", result.stdout)
        self.assertFalse((self.output_dir / "RESCUE_EVIDENCE.json").exists())

        config = rescue_project.normalize_input(self.root, self._input())
        artifacts = rescue_project.build_bundle(
            self.root, config, self.output_dir, "private", "worktree", 50_000, 1_000_000
        )
        evidence = json.loads(artifacts["RESCUE_EVIDENCE.json"])
        documents = evidence["whitebox"]["documents"]["items"]
        self.assertIn("README.md", documents)
        self.assertNotIn("project-os/ignored-os-doc.md", documents)
        self.assertEqual(evidence["whitebox"]["coverage"]["excluded_prefixes"], ["project-os"])

    def test_plan_write_is_deterministic_and_verify_passes(self) -> None:
        args = (
            "plan",
            "--input",
            "project-os/rescue/RESCUE_INPUT.json",
            "--write",
            "--summary",
        )
        first = self._run(*args)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertIn("READY_FOR_LINEAR_APPROVAL", first.stdout)
        snapshots = {
            name: (self.output_dir / name).read_bytes()
            for name in rescue_project.OUTPUT_FILES
        }

        second = self._run(*args)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        for name, content in snapshots.items():
            self.assertEqual(content, (self.output_dir / name).read_bytes())

        verified = self._run(
            "verify", "--input", "project-os/rescue/RESCUE_INPUT.json"
        )
        self.assertEqual(verified.returncode, 0, verified.stdout + verified.stderr)
        self.assertIn("[PASS]", verified.stdout)

    def test_custom_output_directory_keeps_artifact_references_portable(self) -> None:
        custom_output = self.root / "project-os" / "runtime" / "custom-rescue"
        result = self._run(
            "plan",
            "--input",
            "project-os/rescue/RESCUE_INPUT.json",
            "--output-dir",
            "project-os/runtime/custom-rescue",
            "--write",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        linear_import = (custom_output / "LINEAR_RESCUE_IMPORT.json").read_text(
            encoding="utf-8"
        )
        roadmap = (custom_output / "RECOVERY_ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("selected rescue output directory", linear_import)
        self.assertIn("RESCUE_DIAGNOSIS.md", linear_import)
        self.assertIn("selected rescue output directory", roadmap)
        self.assertNotIn("project-os/rescue/RESCUE_DIAGNOSIS.md", linear_import)
        self.assertNotIn("generated `project-os/rescue/` evidence", roadmap)

    def test_safety_block_is_routed_without_emitting_secret_value(self) -> None:
        actual_value = "-".join(["actual", "production", "credential", "928374"])
        self._write(".env", f"API_TOKEN={actual_value}\n")
        result = self._run(
            "plan",
            "--input",
            "project-os/rescue/RESCUE_INPUT.json",
            "--write",
            "--summary",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SAFETY_BLOCKED", result.stdout)
        combined = "".join(
            (self.output_dir / name).read_text(encoding="utf-8")
            for name in rescue_project.OUTPUT_FILES
        )
        self.assertNotIn(actual_value, combined)
        evidence = json.loads((self.output_dir / "RESCUE_EVIDENCE.json").read_text())
        self.assertGreater(evidence["summary"]["safety_block"], 0)
        self.assertEqual(evidence["safety_boundary"]["secret_values_emitted"], False)

    def test_declared_contradiction_routes_to_human_and_linear_dry_run(self) -> None:
        value = self._input()
        value["human_gates"]["baseline_confirmed"] = False  # type: ignore[index]
        value["findings"] = [
            {
                "finding_id": "DOC-RUN-001",
                "title_en": "Documented and implemented startup paths disagree",
                "title_zh": "文档与实现的启动路径冲突",
                "state": "contradicted",
                "impact": "high",
                "confidence": "high",
                "evidence": ["README.md", "src/main.py"],
                "action_steps_en": "Reproduce both startup paths in an isolated environment.",
                "action_steps_zh": "在隔离环境复现两条启动路径。",
                "expected_result_en": "One canonical startup path is proven and documented.",
                "expected_result_zh": "证明并记录一条权威启动路径。",
                "next_verification_en": "Run both commands and record exit status.",
                "next_verification_zh": "运行两条命令并记录退出状态。",
                "recommended_disposition": "decision",
                "owner": "Owner",
                "blocks": ["baseline", "development"],
                "resolved": False,
            }
        ]
        self._write_input(value)
        result = self._run(
            "plan", "--input", "project-os/rescue/RESCUE_INPUT.json", "--write", "--summary"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NEEDS_HUMAN_DECISION", result.stdout)
        import_plan = json.loads((self.output_dir / "LINEAR_RESCUE_IMPORT.json").read_text())
        self.assertEqual(import_plan["mode"], "dry-run")
        self.assertEqual(import_plan["writes_performed"], 0)
        record = next(
            item for item in import_plan["proposed_records"] if item["source_finding"] == "DOC-RUN-001"
        )
        self.assertEqual(record["project"], "Mature Fixture")
        self.assertEqual(record["milestone"], "v1.0.0")
        self.assertIn("文档与实现", record["title"])
        self.assertTrue(record["action_steps"]["en"])
        self.assertTrue(record["action_steps"]["zh"])

    def test_verify_detects_product_evidence_drift(self) -> None:
        result = self._run(
            "plan", "--input", "project-os/rescue/RESCUE_INPUT.json", "--write"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self._write("src/another.py", "print('new')\n")
        verified = self._run(
            "verify", "--input", "project-os/rescue/RESCUE_INPUT.json"
        )
        self.assertEqual(verified.returncode, 1, verified.stdout + verified.stderr)
        self.assertIn("Stale", verified.stdout)

    def test_input_and_output_boundaries_fail_closed(self) -> None:
        value = self._input()
        value["raw"] = "not allowed"
        with self.assertRaises(rescue_project.RescueError):
            rescue_project.normalize_input(self.root, value)
        with self.assertRaises(rescue_project.RescueError):
            rescue_project.resolve_under_root(self.root, "../outside")

    def test_representative_messy_project_certification_is_deterministic(self) -> None:
        actual_value = "-".join(["production", "credential", "material", "498273"])
        (self.root / "package-lock.json").unlink()
        (self.root / "tests" / "test_app.py").unlink()
        (self.root / ".github" / "workflows" / "test.yml").unlink()
        self._write(".env", f"API_TOKEN={actual_value}\n")
        value = self._input()
        value["human_gates"]["baseline_confirmed"] = False  # type: ignore[index]
        value["findings"] = [
            {
                "finding_id": "DOC-RUN-001",
                "title_en": "Documented and implemented startup paths disagree",
                "title_zh": "文档与实现的启动路径冲突",
                "state": "contradicted",
                "impact": "high",
                "confidence": "high",
                "evidence": ["README.md", "src/main.py"],
                "action_steps_en": "Reproduce both startup paths in isolation.",
                "action_steps_zh": "在隔离环境复现两条启动路径。",
                "expected_result_en": "One canonical startup path is proven.",
                "expected_result_zh": "证明一条权威启动路径。",
                "next_verification_en": "Run both candidate commands.",
                "next_verification_zh": "运行两条候选命令。",
                "recommended_disposition": "decision",
                "owner": "Owner",
                "blocks": ["baseline", "development"],
                "resolved": False,
            }
        ]
        self._write_input(value)
        args = (
            "plan", "--input", "project-os/rescue/RESCUE_INPUT.json", "--write", "--summary"
        )
        first = self._run(*args)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        snapshots = {
            name: (self.output_dir / name).read_bytes()
            for name in rescue_project.OUTPUT_FILES
        }
        second = self._run(*args)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        for name, content in snapshots.items():
            self.assertEqual(content, (self.output_dir / name).read_bytes())

        combined = b"".join(snapshots.values()).decode("utf-8")
        self.assertNotIn(actual_value, combined)
        evidence = json.loads(snapshots["RESCUE_EVIDENCE.json"])
        finding_ids = {item["finding_id"] for item in evidence["findings"]}
        self.assertEqual(evidence["pm"]["gate"], "SAFETY_BLOCKED")
        self.assertIn("DOC-RUN-001", finding_ids)
        self.assertIn("DEP-LOCK-001", finding_ids)
        self.assertIn("TEST-001", finding_ids)
        self.assertIn("CI-001", finding_ids)
        self.assertTrue(any(item.startswith("SAF-") for item in finding_ids))
        import_plan = json.loads(snapshots["LINEAR_RESCUE_IMPORT.json"])
        self.assertEqual(import_plan["writes_performed"], 0)
        self.assertTrue(import_plan["one_project_rule"])

    def test_automatic_finding_can_close_with_repository_evidence(self) -> None:
        (self.root / "package.json").unlink()
        (self.root / "package-lock.json").unlink()
        value = self._input()
        value["resolutions"] = [
            {
                "finding_id": "DEP-001",
                "resolution_en": "This repository is intentionally dependency-free.",
                "resolution_zh": "本仓库按设计不使用第三方依赖。",
                "resolved_by": "Owner",
                "resolution_evidence": ["README.md"],
            }
        ]
        self._write_input(value)
        result = self._run(
            "plan", "--input", "project-os/rescue/RESCUE_INPUT.json", "--write", "--summary"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        evidence = json.loads((self.output_dir / "RESCUE_EVIDENCE.json").read_text())
        dependency = next(item for item in evidence["findings"] if item["finding_id"] == "DEP-001")
        self.assertTrue(dependency["resolved"])
        self.assertEqual(dependency["resolution_evidence"], ["README.md"])
        import_plan = json.loads((self.output_dir / "LINEAR_RESCUE_IMPORT.json").read_text())
        self.assertNotIn("DEP-001", {item["source_finding"] for item in import_plan["proposed_records"]})

    def test_current_safety_finding_cannot_be_signed_away(self) -> None:
        actual_value = "-".join(["actual", "production", "credential", "872364"])
        self._write(".env", f"API_TOKEN={actual_value}\n")
        value = self._input()
        value["resolutions"] = [
            {
                "finding_id": "SAF-0001",
                "resolution_en": "Ignore the current safety finding.",
                "resolution_zh": "忽略当前安全发现。",
                "resolved_by": "Owner",
                "resolution_evidence": ["README.md"],
            }
        ]
        self._write_input(value)
        result = self._run(
            "plan", "--input", "project-os/rescue/RESCUE_INPUT.json", "--write"
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot be resolved while the current scan still emits it", result.stderr)


if __name__ == "__main__":
    unittest.main()
