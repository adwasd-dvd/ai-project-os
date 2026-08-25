#!/usr/bin/env python3
"""Tests for deterministic release and recovery controls."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("release_project.py")
SPEC = importlib.util.spec_from_file_location("release_project", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("Cannot load release_project.py")
release_project = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = release_project
SPEC.loader.exec_module(release_project)


class ReleaseProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        for name in ["impact.md", "safety.md", "tests.md", "package.md", "uat.md"]:
            (self.root / name).write_text(
                "Development Gate: `READY`\nfixture\n", encoding="utf-8"
            )
        self.trace = {
            "schema_version": 2,
            "release": {
                "version": "v0.8.0",
                "status": "candidate",
                "uat_status": "pass",
                "uat": {
                    "status": "pass",
                    "evidence": "uat.md",
                    "actor": "Owner",
                    "date": "2026-08-25",
                    "scenarios": ["UAT-0801"],
                    "limitations_disposition": "Accepted",
                },
                "post_release": {"status": "pending"},
                "branch": "codex/v0.8-fixture",
                "pr_url": "https://github.com/example/os/pull/1",
                "tag": None,
                "release_url": None,
            },
            "features": [
                {
                    "feature_id": "DEMO-001",
                    "target_version": "v0.8.0",
                    "state": "accepted",
                    "linear_issue": "EX-101",
                    "requirement_sources": ["tests.md"],
                    "change_impact": "impact.md",
                    "code_paths": ["tests.md"],
                    "evidence_paths": [],
                    "tests": [{"id": "TEST", "path": "tests.md", "status": "pass"}],
                    "uat": {
                        "status": "pass",
                        "evidence": "uat.md",
                        "actor": "Owner",
                        "date": "2026-08-25",
                        "scenarios": ["UAT-0801"],
                        "limitations_disposition": "Accepted",
                    },
                    "decisions": [],
                    "risks": [],
                }
            ],
        }
        (self.root / "trace.json").write_text(
            json.dumps(self.trace), encoding="utf-8"
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def release_input(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "version": "v0.8.0",
            "summary": "Fixture release / Fixture 发布",
            "scope": {"included": ["DEMO-001"], "excluded": [], "deferred": []},
            "traceability_manifest": "trace.json",
            "change_impact_report": "impact.md",
            "safety": {
                "profile": "private",
                "destination": "fixture GitHub Release",
                "decision": "Go",
                "block_findings": 0,
                "review_findings": 0,
                "review_disposition": "None",
                "evidence": "safety.md",
            },
            "tests": [{"id": "FULL", "status": "pass", "evidence": "tests.md"}],
            "package": {
                "asset": "ai-project-os-v0.8.0.zip",
                "sha256": "a" * 64,
                "deterministic": True,
                "extracted_validation": "pass",
                "evidence": "package.md",
            },
            "rollback": {
                "target": "v0.6.0",
                "plan": "Install prior immutable package on a branch.",
                "authority": "Owner",
                "verification": "Run validator and tests.",
            },
            "known_limitations": [],
            "github": {
                "branch": "codex/v0.8-fixture",
                "pr_url": "https://github.com/example/os/pull/1",
                "tag": None,
                "release_url": None,
            },
        }

    def test_ready_plan_and_notes_are_deterministic(self) -> None:
        value = self.release_input()
        first = release_project.validate_release_input(value, self.root)
        second = release_project.validate_release_input(value, self.root)
        self.assertEqual(([], []), first[:2])
        self.assertEqual(first[:2], second[:2])
        report = release_project.render_readiness(value, first[0], first[1], first[2])
        notes = release_project.render_release_notes(value, first[2])
        self.assertIn("Gate: `READY`", report)
        self.assertIn("DEMO-001", notes)

    def test_pending_human_uat_blocks_readiness(self) -> None:
        self.trace["release"]["uat_status"] = "pending"
        self.trace["release"]["uat"] = {"status": "pending"}
        self.trace["features"][0]["state"] = "uat_pending"
        self.trace["features"][0]["uat"] = {
            "status": "pending",
            "evidence": "uat.md",
            "scenarios": ["UAT-0801"],
        }
        (self.root / "trace.json").write_text(json.dumps(self.trace), encoding="utf-8")
        findings, blockers, _ = release_project.validate_release_input(
            self.release_input(), self.root
        )
        self.assertEqual([], findings)
        self.assertTrue(any("Human version UAT" in item for item in blockers))

    def test_safety_package_and_rollback_fail_closed(self) -> None:
        value = self.release_input()
        value["safety"]["decision"] = "Review"
        value["package"]["deterministic"] = False
        value["rollback"]["target"] = ""
        _, blockers, _ = release_project.validate_release_input(value, self.root)
        self.assertTrue(any("Safety" in item for item in blockers))
        self.assertTrue(any("deterministic" in item for item in blockers))
        self.assertTrue(any("rollback.target" in item for item in blockers))

    def test_scope_must_match_traceability(self) -> None:
        value = self.release_input()
        value["scope"]["included"].append("DEMO-002")
        _, blockers, _ = release_project.validate_release_input(value, self.root)
        self.assertTrue(any("exactly match" in item for item in blockers))

    def test_feedback_classification_covers_handoff_categories(self) -> None:
        base = {
            "schema_version": 1,
            "kind": "bug",
            "original_scope_complete": True,
            "blocks_current_uat": False,
            "affects_released_version": False,
            "requires_business_decision": False,
            "later_version_feedback": True,
            "severity": "medium",
        }
        self.assertEqual("carry_over", release_project.classify_feedback(base)["classification"])
        base["later_version_feedback"] = False
        base["affects_released_version"] = True
        base["severity"] = "high"
        self.assertEqual("hotfix", release_project.classify_feedback(base)["classification"])
        base["requires_business_decision"] = True
        self.assertEqual("decision", release_project.classify_feedback(base)["classification"])

    def post_release_input(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "version": "v0.8.0",
            "tag": "v0.8.0",
            "release_url": "https://github.com/example/os/releases/tag/v0.8.0",
            "local_sha256": "b" * 64,
            "remote_sha256": "b" * 64,
            "rollback_target": "v0.6.0",
            "checks": [
                {"id": "ASSET", "status": "pass", "evidence": "digest match"},
                {"id": "LINEAR", "status": "pass", "evidence": "project complete"},
            ],
        }

    def test_post_release_receipt_passes_and_is_sanitized(self) -> None:
        value = self.post_release_input()
        findings, blockers = release_project.validate_post_release(value, self.root)
        self.assertEqual(([], []), (findings, blockers))
        report = release_project.render_post_release(value, findings, blockers)
        self.assertIn("Result: `PASS`", report)
        self.assertNotIn("raw_payload", report)

    def test_post_release_digest_mismatch_blocks(self) -> None:
        value = self.post_release_input()
        value["remote_sha256"] = "c" * 64
        _, blockers = release_project.validate_post_release(value, self.root)
        self.assertTrue(any("does not match" in item for item in blockers))

    def test_sensitive_raw_fields_are_rejected(self) -> None:
        value = self.post_release_input()
        value["raw_payload"] = {"secret": "not emitted"}
        findings, _ = release_project.validate_post_release(value, self.root)
        self.assertTrue(any("Forbidden" in item for item in findings))


if __name__ == "__main__":
    unittest.main()
