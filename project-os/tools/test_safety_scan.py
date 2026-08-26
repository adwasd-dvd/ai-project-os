#!/usr/bin/env python3
"""Tests for the sanitized AI Project OS repository-safety scanner."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCANNER = Path(__file__).with_name("safety_scan.py")


def run_scan(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCANNER), "--root", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    )


class SafetyScanTests(unittest.TestCase):
    def test_default_scan_is_read_only_and_never_emits_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            provider_token = "ghp_" + "A" * 24
            assigned_value = "live_" + "value_" + "9" * 16
            (root / "app.py").write_text(
                f'PROVIDER_TOKEN = "{provider_token}"\nAPI_KEY = "{assigned_value}"\n',
                encoding="utf-8",
            )

            result = run_scan(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(provider_token, result.stdout)
            self.assertNotIn(assigned_value, result.stdout)
            evidence = json.loads(result.stdout)
            rules = {item["rule_id"] for item in evidence["findings"]}
            self.assertIn("SAF003", rules)
            self.assertIn("SAF004", rules)
            self.assertFalse(evidence["safety"]["matched_values_emitted"])
            self.assertFalse(evidence["safety"]["source_lines_emitted"])
            self.assertFalse((root / "project-os" / "safety" / "SAFETY_EVIDENCE.json").exists())

    def test_placeholders_and_env_templates_do_not_create_secret_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env.example").write_text(
                "API_KEY=your_api_key_here\nPASSWORD=changeme\n", encoding="utf-8"
            )
            (root / "README.md").write_text(
                "Use /Users/<user>/work or /home/.../work as examples.\n",
                encoding="utf-8",
            )
            (root / "runtime-config.js").write_text(
                'const apiKey = context.env.GOOGLE_MAPS_API_KEY || "";\n',
                encoding="utf-8",
            )

            result = run_scan(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            evidence = json.loads(result.stdout)
            self.assertEqual(evidence["findings"], [])

    def test_profile_changes_absolute_path_disposition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            private_path = "/Users/" + "alice" + "/work/acme"
            (root / "notes.md").write_text(private_path, encoding="utf-8")

            private = run_scan(root, "--profile", "private")
            public = run_scan(
                root, "--profile", "public", "--fail-on-block"
            )

            self.assertEqual(private.returncode, 0, private.stderr)
            private_evidence = json.loads(private.stdout)
            self.assertEqual(private_evidence["findings"][0]["disposition"], "info")
            self.assertEqual(public.returncode, 2, public.stderr)
            public_evidence = json.loads(public.stdout)
            self.assertEqual(public_evidence["findings"][0]["disposition"], "block")
            self.assertNotIn(private_path, public.stdout)

    def test_staged_scope_only_scans_staged_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            git(root, "init", "-q")
            git(root, "config", "user.email", "test@example.com")
            git(root, "config", "user.name", "Safety Test")
            (root / "tracked.txt").write_text("safe\n", encoding="utf-8")
            git(root, "add", "tracked.txt")
            git(root, "commit", "-qm", "initial")

            staged_value = "stage_" + "secret_" + "8" * 16
            untracked_value = "other_" + "secret_" + "7" * 16
            (root / "tracked.txt").write_text(
                f'PASSWORD="{staged_value}"\n', encoding="utf-8"
            )
            (root / "untracked.txt").write_text(
                f'TOKEN="{untracked_value}"\n', encoding="utf-8"
            )
            git(root, "add", "tracked.txt")

            result = run_scan(root, "--scope", "staged", "--profile", "private")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn(staged_value, result.stdout)
            self.assertNotIn(untracked_value, result.stdout)
            evidence = json.loads(result.stdout)
            self.assertEqual({item["path"] for item in evidence["findings"]}, {"tracked.txt"})
            self.assertTrue(all(item["staged"] for item in evidence["findings"]))

    def test_write_check_is_deterministic_and_output_is_confined(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("safe\n", encoding="utf-8")

            write = run_scan(root, "--profile", "private", "--write")
            check = run_scan(root, "--profile", "private", "--check")
            outside = run_scan(
                root,
                "--output-dir",
                str(root.parent / "outside-safety-output"),
                "--write",
            )

            evidence_path = root / "project-os" / "safety" / "SAFETY_EVIDENCE.json"
            self.assertEqual(write.returncode, 0, write.stderr)
            self.assertTrue(evidence_path.exists())
            self.assertEqual(check.returncode, 0, check.stderr)
            self.assertEqual(outside.returncode, 1)
            self.assertIn("inside the repository root", outside.stderr)

    def test_explicit_prefix_exclusion_is_recorded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "project-os").mkdir()
            sensitive_value = "-".join(["actual", "sensitive", "value", "12345"])
            (root / "project-os" / "private.env").write_text(
                f"PASSWORD={sensitive_value}\n", encoding="utf-8"
            )
            (root / "README.md").write_text("safe\n", encoding="utf-8")

            result = run_scan(root, "--profile", "private", "--exclude-prefix", "project-os")

            self.assertEqual(result.returncode, 0, result.stderr)
            evidence = json.loads(result.stdout)
            self.assertEqual(evidence["findings"], [])
            self.assertEqual(evidence["excluded_prefixes"], ["project-os"])
            self.assertGreater(evidence["skipped"]["requested_prefixes"], 0)

    def test_invalid_prefix_exclusion_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = run_scan(root, "--exclude-prefix", "../outside")
            self.assertEqual(result.returncode, 1)
            self.assertIn("Invalid exclusion prefix", result.stderr)


if __name__ == "__main__":
    unittest.main()
