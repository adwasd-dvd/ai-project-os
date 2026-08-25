#!/usr/bin/env python3
"""Tests for traceability and change-impact validation."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("trace_project.py")
SPEC = importlib.util.spec_from_file_location("trace_project", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("Cannot load trace_project.py")
trace_project = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(trace_project)


class TraceProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for path in ["requirements.md", "impact.json", "src/app.py", "tests/test_app.py", "uat.md"]:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("fixture\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def manifest(self, state: str = "uat_pending") -> dict[str, object]:
        return {
            "schema_version": 1,
            "release": {
                "version": "v0.6.0",
                "status": "candidate",
                "uat_status": "pending",
                "branch": "codex/v0.6-fixture",
                "pr_url": None,
                "tag": None,
                "release_url": None,
            },
            "features": [
                {
                    "feature_id": "DEMO-001",
                    "target_version": "v0.6.0",
                    "state": state,
                    "linear_issue": "EX-101",
                    "requirement_sources": ["requirements.md"],
                    "change_impact": "impact.json",
                    "code_paths": ["src/app.py"],
                    "evidence_paths": [],
                    "tests": [{"id": "TEST-001", "path": "tests/test_app.py", "status": "pass"}],
                    "uat": {"status": "pending", "evidence": None},
                    "decisions": ["DEC-001"],
                    "risks": ["RISK-001"],
                }
            ],
        }

    def valid_impact(self) -> dict[str, object]:
        impacts = []
        for area in sorted(trace_project.REQUIRED_IMPACT_AREAS):
            impacts.append(
                {
                    "area": area,
                    "level": "medium",
                    "confidence": "high",
                    "claim": f"Fixture impact for {area}",
                    "evidence": "Fixture evidence",
                    "evidence_path": "requirements.md",
                    "next_verification": "Run fixture verification",
                }
            )
        return {
            "schema_version": 1,
            "feature_id": "DEMO-001",
            "target_version": "v0.6.0",
            "scope_change": False,
            "unresolved_decisions": [],
            "impacts": impacts,
            "test_plan": ["Run tests"],
            "uat_plan": ["Owner UAT"],
            "rollout": "Use a candidate branch",
            "rollback": "Return to prior tag",
        }

    def test_uat_pending_manifest_passes_without_claiming_acceptance(self) -> None:
        manifest = self.manifest()
        findings = trace_project.validate_manifest(manifest, self.root)
        self.assertEqual([], findings)
        report = trace_project.render_traceability(manifest, findings)
        self.assertIn("Result: `PASS`", report)
        self.assertIn("Automated tests never count as human UAT", report)

    def test_accepted_requires_human_uat_evidence(self) -> None:
        manifest = self.manifest("accepted")
        findings = trace_project.validate_manifest(manifest, self.root)
        self.assertTrue(any("human UAT pass" in item for item in findings))
        self.assertTrue(any("UAT evidence" in item for item in findings))

    def test_released_requires_tag_release_and_release_uat(self) -> None:
        manifest = self.manifest("released")
        feature = manifest["features"][0]
        feature["uat"] = {"status": "pass", "evidence": "uat.md"}
        findings = trace_project.validate_manifest(manifest, self.root)
        self.assertTrue(any("release.uat_status" in item for item in findings))
        self.assertTrue(any("tag and release_url" in item for item in findings))

    def test_valid_change_impact_is_ready(self) -> None:
        value = self.valid_impact()
        findings, blockers = trace_project.validate_impact(value, self.root)
        self.assertEqual([], findings)
        self.assertEqual([], blockers)
        report = trace_project.render_impact(value, findings, blockers)
        self.assertIn("Development Gate: `READY`", report)
        self.assertIn("Test Impact / 测试影响", report)
        self.assertIn("Human UAT Impact / 人工 UAT 影响", report)

    def test_high_impact_low_confidence_and_scope_change_block(self) -> None:
        value = self.valid_impact()
        value["scope_change"] = True
        value["unresolved_decisions"] = ["DEC-009"]
        value["impacts"][0]["level"] = "high"
        value["impacts"][0]["confidence"] = "low"
        findings, blockers = trace_project.validate_impact(value, self.root)
        self.assertEqual([], findings)
        self.assertEqual(3, len(blockers))
        self.assertIn("Development Gate: `BLOCKED`", trace_project.render_impact(value, findings, blockers))

    def test_missing_evidence_path_is_reported(self) -> None:
        manifest = self.manifest()
        manifest["features"][0]["code_paths"] = ["src/missing.py"]
        findings = trace_project.validate_manifest(manifest, self.root)
        self.assertTrue(any("missing path" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
