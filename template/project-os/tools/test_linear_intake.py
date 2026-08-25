#!/usr/bin/env python3
"""Tests for deterministic Linear intake and guarded writes."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("linear_intake.py")
SPEC = importlib.util.spec_from_file_location("linear_intake", SCRIPT)
if SPEC is None or SPEC.loader is None:  # pragma: no cover
    raise RuntimeError("Cannot load linear_intake.py")
linear_intake = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = linear_intake
SPEC.loader.exec_module(linear_intake)


class FakeClient:
    def __init__(self, fail_once: set[str] | None = None) -> None:
        self.calls: list[str] = []
        self.fail_once = fail_once or set()

    def apply_action(self, action: dict[str, object]) -> str:
        key = str(action["idempotency_key"])
        self.calls.append(key)
        if key in self.fail_once:
            self.fail_once.remove(key)
            raise linear_intake.IntakeError("fixture failure")
        return f"result-{len(self.calls)}"


class LinearIntakeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.project_os = Path(__file__).resolve().parents[1]
        self.root = self.project_os.parent
        self.config = linear_intake.read_json(
            self.project_os / "automation" / "linear_intake.example.json"
        )
        self.snapshot = linear_intake.read_json(
            self.project_os / "automation" / "fixtures" / "train_a_snapshot.json"
        )
        self.as_of = datetime(2026, 8, 24, 18, 0, tzinfo=timezone.utc)

    def test_scan_routes_every_queue_and_closed_watch(self) -> None:
        report = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)

        self.assertEqual(["EX-901"], [x["identifier"] for x in report["queues"]["codex_queue"]])
        self.assertEqual(["EX-902"], [x["identifier"] for x in report["queues"]["human_queue"]])
        self.assertEqual(["EX-903"], [x["identifier"] for x in report["queues"]["review_queue"]])
        self.assertEqual(["EX-904"], [x["identifier"] for x in report["queues"]["inconsistent"]])
        self.assertEqual(["EX-905"], [x["identifier"] for x in report["queues"]["closed_watch"]])
        self.assertEqual("carry_over_revalidation", report["queues"]["closed_watch"][0]["feedback"])
        self.assertEqual(["EX-906"], [x["identifier"] for x in report["queues"]["blocked_ambiguous"]])
        self.assertEqual("OTHER-999", report["skipped"][0]["identifier"])
        self.assertEqual("None. Dry run only. / 无写入，仅 dry-run。", report["write_actions"])

    def test_report_is_deterministic_and_bilingual(self) -> None:
        first = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)
        second = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)
        self.assertEqual(first, second)
        markdown = linear_intake.render_markdown(first)
        self.assertIn("Scan Scope / 扫描范围", markdown)
        self.assertIn("Created / 已创建", markdown)
        self.assertIn("Updated / 已更新", markdown)
        self.assertIn("Skipped / 已跳过", markdown)
        self.assertIn("Blockers / 阻塞项", markdown)
        self.assertIn("Next Action / 下一步", markdown)

    def test_pre_completion_comment_does_not_enter_closed_watch(self) -> None:
        issue = json.loads(json.dumps(self.snapshot["issues"][4]))
        issue["comments"][0]["created_at"] = "2026-08-09T12:00:00Z"
        issue["comments"][0]["updated_at"] = "2026-08-09T12:00:00Z"
        self.assertIsNone(
            linear_intake.latest_recent_comment(
                issue, datetime(2026, 8, 1, tzinfo=timezone.utc)
            )
        )

    def test_advisory_key_ignores_issue_timestamp_and_remote_marker_deduplicates(self) -> None:
        first_snapshot = json.loads(json.dumps(self.snapshot))
        first = linear_intake.scan_snapshot(first_snapshot, self.config, self.as_of)
        issue_key = next(
            action["idempotency_key"]
            for action in first["planned_actions"]
            if action["target_id"] == "issue-904"
        )

        second_snapshot = json.loads(json.dumps(self.snapshot))
        issue = second_snapshot["issues"][3]
        issue["updated_at"] = "2026-08-24T18:01:00Z"
        second = linear_intake.scan_snapshot(second_snapshot, self.config, self.as_of)
        second_key = next(
            action["idempotency_key"]
            for action in second["planned_actions"]
            if action["target_id"] == "issue-904"
        )
        self.assertEqual(issue_key, second_key)

        issue["comments"].append(
            {
                "id": "automation-comment",
                "body": f"advisory\n<!-- {issue_key} -->",
                "created_at": "2026-08-24T18:02:00Z",
                "updated_at": "2026-08-24T18:02:00Z",
            }
        )
        third = linear_intake.scan_snapshot(second_snapshot, self.config, self.as_of)
        self.assertNotIn(issue_key, [item["idempotency_key"] for item in third["planned_actions"]])

    def test_live_scan_fails_closed_without_credentials(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["team"]["id"] = "fixture-team"
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(linear_intake.IntakeError):
                linear_intake.load_live_snapshot(config)

    def test_config_rejects_non_linear_auth_endpoint(self) -> None:
        config = json.loads(json.dumps(self.config))
        config["auth"]["endpoint"] = "https://example.invalid/graphql"
        with self.assertRaises(linear_intake.IntakeError):
            linear_intake.validate_config(config)

    def test_config_rejects_invalid_runtime_controls(self) -> None:
        invalid_values = [
            ("lookback_days", "7"),
            ("max_issues", True),
            ("auth.token_env", "NOT VALID"),
            ("retry.max_retries", 6),
            ("retry.timeout_seconds", 0),
            ("write_policy.runtime_authorization_env", "ALSO-NOT-VALID"),
        ]
        for field, value in invalid_values:
            with self.subTest(field=field):
                config = json.loads(json.dumps(self.config))
                target = config
                parts = field.split(".")
                for part in parts[:-1]:
                    target = target[part]
                target[parts[-1]] = value
                with self.assertRaises(linear_intake.IntakeError):
                    linear_intake.validate_config(config)

    def test_client_refuses_redirects(self) -> None:
        handler = linear_intake.NoRedirect()
        request = mock.Mock(full_url=linear_intake.API_URL)
        with self.assertRaises(urllib.error.HTTPError) as raised:
            handler.redirect_request(
                request,
                mock.Mock(),
                302,
                "Found",
                {},
                "https://example.invalid/graphql",
            )
        self.assertEqual(302, raised.exception.code)

    def test_live_normalization_keeps_blocking_relations(self) -> None:
        issue = linear_intake.normalize_live_issue(
            {
                "id": "issue-1",
                "identifier": "EX-1",
                "title": "Fixture",
                "state": {"name": "Todo", "type": "unstarted"},
                "labels": {"nodes": []},
                "comments": {"nodes": []},
                "inverseRelations": {
                    "nodes": [
                        {
                            "type": "blocks",
                            "issue": {"id": "decision-1", "identifier": "EX-2"},
                        },
                        {
                            "type": "related",
                            "issue": {"id": "related-1", "identifier": "EX-3"},
                        },
                    ]
                },
            }
        )
        self.assertEqual(["EX-2"], [item["identifier"] for item in issue["blocked_by"]])

    def test_nested_connection_pagination_marks_live_scan_partial(self) -> None:
        client = linear_intake.LinearClient(token="fixture")
        node = {
            "id": "issue-1",
            "identifier": "EX-1",
            "title": "Fixture",
            "state": {"name": "Todo", "type": "unstarted"},
            "labels": {"nodes": [], "pageInfo": {"hasNextPage": False}},
            "comments": {"nodes": [], "pageInfo": {"hasNextPage": True}},
            "inverseRelations": {
                "nodes": [],
                "pageInfo": {"hasNextPage": False},
            },
        }
        response = {
            "team": {
                "id": "team-1",
                "name": "Example Team",
                "key": "EX",
                "issues": {
                    "nodes": [node],
                    "pageInfo": {"hasNextPage": False, "endCursor": None},
                },
            }
        }
        with mock.patch.object(client, "execute", return_value=response):
            snapshot = client.fetch_snapshot("team-1", 50)
        self.assertTrue(snapshot["partial"])
        self.assertIn("EX-1.comments", snapshot["partial_reason"])

    def test_live_scope_resolves_current_and_adjacent_projects(self) -> None:
        client = linear_intake.LinearClient(token="fixture")

        def response(query: str, variables: dict[str, object]) -> dict[str, object]:
            if "IntakeProjects" in query:
                return {
                    "team": {
                        "id": "team-1",
                        "name": "Example Team",
                        "key": "EX",
                        "projects": {
                            "nodes": [
                                {"id": "p06", "name": "Example Product v0.6"},
                                {"id": "p05", "name": "Example Product v0.5"},
                                {"id": "other", "name": "Other Product"},
                            ],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        },
                    }
                }
            identifier = "EX-6" if variables["projectId"] == "p06" else "EX-5"
            return {
                "project": {
                    "issues": {
                        "nodes": [
                            {
                                "id": f"id-{identifier}",
                                "identifier": identifier,
                                "title": "Fixture",
                                "state": {"name": "Todo", "type": "unstarted"},
                                "project": {
                                    "id": variables["projectId"],
                                    "name": "Example Product",
                                },
                                "labels": {"nodes": []},
                                "comments": {"nodes": []},
                                "inverseRelations": {"nodes": []},
                            }
                        ],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            }

        with mock.patch.object(client, "execute", side_effect=response):
            snapshot = client.fetch_scoped_snapshot(
                "team-1", 50, ["Example Product v0.6"], ["Example Product"], []
            )

        self.assertFalse(snapshot["partial"])
        self.assertEqual(["EX-5", "EX-6"], [item["identifier"] for item in snapshot["issues"]])
        self.assertEqual(2, len(snapshot["resolved_projects"]))

    def test_partial_live_scope_blocks_actions_and_apply(self) -> None:
        snapshot = json.loads(json.dumps(self.snapshot))
        snapshot["partial"] = True
        snapshot["partial_reason"] = "fixture limit reached"
        report = linear_intake.scan_snapshot(snapshot, self.config, self.as_of)
        self.assertFalse(report["scan_complete"])
        self.assertEqual([], report["planned_actions"])
        self.assertEqual("SCAN", report["blockers"][0]["identifier"])

        enabled = json.loads(json.dumps(self.config))
        enabled["write_policy"]["enabled"] = True
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.dict(os.environ, {"AIPOS_LINEAR_WRITE_APPROVED": "1"}):
                with self.assertRaises(linear_intake.IntakeError):
                    linear_intake.apply_plan(
                        report,
                        enabled,
                        FakeClient(),
                        Path(directory) / "ledger.json",
                        authorized=True,
                        now=lambda: self.as_of,
                    )

    def test_apply_requires_all_write_gates(self) -> None:
        plan = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            with self.assertRaises(linear_intake.IntakeError):
                linear_intake.apply_plan(plan, self.config, FakeClient(), ledger, authorized=True, now=lambda: self.as_of)

            enabled = json.loads(json.dumps(self.config))
            enabled["write_policy"]["enabled"] = True
            with mock.patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(linear_intake.IntakeError):
                    linear_intake.apply_plan(plan, enabled, FakeClient(), ledger, authorized=True, now=lambda: self.as_of)

    def test_idempotency_survives_restart_and_ledger_is_sanitized(self) -> None:
        plan = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)
        enabled = json.loads(json.dumps(self.config))
        enabled["write_policy"]["enabled"] = True
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            client = FakeClient()
            with mock.patch.dict(os.environ, {"AIPOS_LINEAR_WRITE_APPROVED": "1"}):
                first = linear_intake.apply_plan(plan, enabled, client, ledger, authorized=True, now=lambda: self.as_of)
                second = linear_intake.apply_plan(plan, enabled, client, ledger, authorized=True, now=lambda: self.as_of)

            self.assertGreater(len(first["applied"]), 0)
            self.assertEqual([], second["applied"])
            self.assertEqual(len(first["applied"]), len(second["skipped"]))
            ledger_text = ledger.read_text(encoding="utf-8")
            self.assertNotIn("Automation advisory", ledger_text)
            self.assertNotIn("LINEAR_API_KEY", ledger_text)

    def test_partial_failure_retries_only_failed_action(self) -> None:
        plan = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)
        enabled = json.loads(json.dumps(self.config))
        enabled["write_policy"]["enabled"] = True
        failing_key = plan["planned_actions"][0]["idempotency_key"]
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            client = FakeClient({failing_key})
            with mock.patch.dict(os.environ, {"AIPOS_LINEAR_WRITE_APPROVED": "1"}):
                first = linear_intake.apply_plan(plan, enabled, client, ledger, authorized=True, now=lambda: self.as_of)
                second = linear_intake.apply_plan(plan, enabled, client, ledger, authorized=True, now=lambda: self.as_of)

            self.assertEqual(1, len(first["failed"]))
            self.assertEqual(1, len(second["applied"]))
            self.assertEqual(failing_key, second["applied"][0]["idempotency_key"])

    def test_invalid_late_action_blocks_before_any_write(self) -> None:
        plan = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)
        enabled = json.loads(json.dumps(self.config))
        enabled["write_policy"]["enabled"] = True
        plan["planned_actions"].append(
            {
                "idempotency_key": "invalid:late",
                "operation": "issue_update",
                "target_id": "issue-901",
                "payload": {"description": "must not be allowed"},
            }
        )
        client = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / "ledger.json"
            with mock.patch.dict(os.environ, {"AIPOS_LINEAR_WRITE_APPROVED": "1"}):
                with self.assertRaises(linear_intake.IntakeError):
                    linear_intake.apply_plan(plan, enabled, client, ledger, authorized=True, now=lambda: self.as_of)
        self.assertEqual([], client.calls)

    def test_stale_plan_fails_before_any_write(self) -> None:
        plan = linear_intake.scan_snapshot(self.snapshot, self.config, self.as_of)
        enabled = json.loads(json.dumps(self.config))
        enabled["write_policy"]["enabled"] = True
        client = FakeClient()
        stale_now = datetime(2026, 8, 24, 20, 0, tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.dict(os.environ, {"AIPOS_LINEAR_WRITE_APPROVED": "1"}):
                with self.assertRaises(linear_intake.IntakeError):
                    linear_intake.apply_plan(
                        plan,
                        enabled,
                        client,
                        Path(directory) / "ledger.json",
                        authorized=True,
                        now=lambda: stale_now,
                    )
        self.assertEqual([], client.calls)

    def test_allowlisted_status_update_can_apply(self) -> None:
        enabled = json.loads(json.dumps(self.config))
        enabled["write_policy"]["enabled"] = True
        enabled["write_policy"]["allowed_operations"] = ["issue_update"]
        enabled["write_policy"]["allowed_update_fields"] = ["stateId"]
        plan = {
            "scan_complete": True,
            "generated_at": self.as_of.isoformat().replace("+00:00", "Z"),
            "actions": [
                {
                    "idempotency_key": "fixture:update-state",
                    "operation": "issue_update",
                    "target_id": "issue-901",
                    "payload": {"stateId": "state-review"},
                }
            ],
        }
        with tempfile.TemporaryDirectory() as directory:
            client = FakeClient()
            with mock.patch.dict(os.environ, {"AIPOS_LINEAR_WRITE_APPROVED": "1"}):
                outcome = linear_intake.apply_plan(
                    plan,
                    enabled,
                    client,
                    Path(directory) / "ledger.json",
                    authorized=True,
                    now=lambda: self.as_of,
                )
        self.assertEqual(1, len(outcome["applied"]))

    def test_issue_create_requires_bilingual_action_and_result_sections(self) -> None:
        policy = {
            "allowed_operations": ["issue_create"],
            "allowed_update_fields": [],
        }
        action = {
            "idempotency_key": "fixture:create",
            "operation": "issue_create",
            "payload": {
                "teamId": "team-1",
                "title": "[DEMO-010] Carry-over",
                "description": "Action Steps / 执行动作\n1. Verify.\nExpected Result / 期待结果\nPass.",
            },
        }
        linear_intake.validate_action(action, policy)
        action["payload"]["description"] = "Action Steps only"
        with self.assertRaises(linear_intake.IntakeError):
            linear_intake.validate_action(action, policy)

    def test_output_path_cannot_escape_repository(self) -> None:
        with self.assertRaises(linear_intake.IntakeError):
            linear_intake.resolve_under_root(self.root, "../outside.json")


if __name__ == "__main__":
    unittest.main()
