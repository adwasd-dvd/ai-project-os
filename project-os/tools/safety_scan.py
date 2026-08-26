#!/usr/bin/env python3
"""Collect deterministic, sanitized repository-safety evidence.

The scanner is read-only unless --write is provided. Findings contain rule IDs,
repository-relative paths, classifications, dispositions, and remediation only.
Matched values and matching source lines are never emitted.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.0"
OUTPUT_NAME = "SAFETY_EVIDENCE.json"
PROFILES = ("local", "private", "team", "public")
SCOPES = ("worktree", "staged", "tracked")
MAX_FILE_BYTES = 1_000_000

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "bower_components",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "vendor",
}

TEXT_SUFFIXES = {
    "",
    ".cfg",
    ".conf",
    ".css",
    ".env",
    ".go",
    ".html",
    ".ini",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".mdx",
    ".php",
    ".properties",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".swift",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

SECRET_FILENAMES = {
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials.json",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
    "service-account.json",
}

SECRET_SUFFIXES = {".key", ".p12", ".pfx", ".pkcs12", ".pem"}
ENV_TEMPLATE_SUFFIXES = (".example", ".sample", ".template")
AGENT_FILENAMES = {
    "agents.md",
    "claude.md",
    "copilot-instructions.md",
    "cursor.md",
    "gemini.md",
}

PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----", re.IGNORECASE
)
PROVIDER_TOKEN_RES = [
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b"),
]
CREDENTIAL_ASSIGNMENT_RE = re.compile(
    r"(?i)[\"']?(?:password|passwd|pwd|secret|token|api[_-]?key|"
    r"access[_-]?key|client[_-]?secret|private[_-]?key|session[_-]?key)"
    r"[\"']?\s*[:=]\s*[\"']?([A-Za-z0-9_./+=:@-]{8,})"
)
CONNECTION_STRING_RE = re.compile(
    r"(?i)\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://"
    r"[^\s/:]+:[^\s/@]+@"
)
ABSOLUTE_USER_PATH_RE = re.compile(
    r"(?:/Users/[^/\s]+/|/home/[^/\s]+/|[A-Za-z]:\\Users\\[^\\\s]+\\)"
)

PLACEHOLDER_MARKERS = {
    "changeme",
    "dummy",
    "example",
    "fake",
    "not-a-secret",
    "placeholder",
    "redacted",
    "replace-me",
    "replace_me",
    "sample",
    "test-only",
    "your-api-key",
    "your_api_key",
    "your-token",
    "your_token",
}

REMEDIATION = {
    "SAF001": "Remove the file from the proposed destination; add an ignore rule and rotate credentials if exposure is possible.",
    "SAF002": "Stop publication and rotate/revoke the private key; review Git history without copying key material.",
    "SAF003": "Stop publication and rotate/revoke the provider credential; record only sanitized incident evidence.",
    "SAF004": "Replace the value with a placeholder or environment lookup and rotate it if it may be active.",
    "SAF005": "Remove the credential-bearing connection string, rotate credentials, and use a named configuration source.",
    "SAF006": "Replace the user-specific absolute path with a repository-relative path or documented placeholder.",
    "SAF007": "Keep raw conversation exports local; record only a sanitized decision or claim summary.",
    "SAF008": "Review project-specific memory before sharing; publish a sanitized summary when detailed evidence is private.",
    "SAF009": "Review the Agent document for personal context, conflicts, internal links, and destination suitability.",
}


class ScanError(RuntimeError):
    """Raised when the scan cannot safely continue."""


def run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def git_paths(root: Path, *args: str) -> set[str]:
    result = run_git(root, *args)
    if result.returncode != 0:
        return set()
    return {item for item in result.stdout.split("\0") if item}


def is_git_repository(root: Path) -> bool:
    result = run_git(root, "rev-parse", "--is-inside-work-tree")
    return result.returncode == 0 and result.stdout.strip() == "true"


def should_skip(relative: Path) -> bool:
    return any(part.lower() in SKIP_DIRS for part in relative.parts[:-1])


def normalize_exclude_prefixes(values: Iterable[str]) -> tuple[str, ...]:
    prefixes: set[str] = set()
    for raw in values:
        value = str(raw).strip().replace("\\", "/").strip("/")
        path = Path(value)
        if not value or value == "." or path.is_absolute() or ".." in path.parts:
            raise ScanError(f"Invalid exclusion prefix: {raw!r}")
        prefixes.add(path.as_posix())
    return tuple(sorted(prefixes))


def excluded_by_prefix(relative: Path, prefixes: Iterable[str]) -> bool:
    value = relative.as_posix()
    return any(value == prefix or value.startswith(prefix + "/") for prefix in prefixes)


def filesystem_paths(root: Path) -> Iterable[str]:
    for current, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(
            directory for directory in dirs if directory.lower() not in SKIP_DIRS
        )
        current_path = Path(current)
        for filename in sorted(files):
            yield (current_path / filename).relative_to(root).as_posix()


def list_scope_files(
    root: Path,
    scope: str,
    output_relative: Path,
    max_files: int,
    exclude_prefixes: tuple[str, ...] = (),
) -> tuple[list[Path], str, int, int, int]:
    is_repo = is_git_repository(root)
    source = "filesystem fallback"

    if scope == "staged":
        if not is_repo:
            raise ScanError("The staged scope requires a Git repository.")
        raw_paths: Iterable[str] = git_paths(
            root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"
        )
        source = "git staged index"
    elif scope == "tracked":
        if not is_repo:
            raise ScanError("The tracked scope requires a Git repository.")
        raw_paths = git_paths(root, "ls-files", "-z")
        source = "git tracked files"
    elif is_repo:
        raw_paths = git_paths(root, "ls-files", "-co", "--exclude-standard", "-z")
        source = "git worktree files"
    else:
        raw_paths = filesystem_paths(root)

    files: list[Path] = []
    symlinks_skipped = 0
    generated_skipped = 0
    requested_skipped = 0
    for raw in sorted(raw_paths):
        relative = Path(raw)
        if not raw or relative.is_absolute() or ".." in relative.parts:
            continue
        if relative == output_relative:
            continue
        if excluded_by_prefix(relative, exclude_prefixes):
            requested_skipped += 1
            continue
        if should_skip(relative):
            generated_skipped += 1
            continue
        absolute = root / relative
        if absolute.is_symlink():
            symlinks_skipped += 1
            continue
        if not absolute.is_file():
            continue
        files.append(relative)
        if len(files) > max_files:
            raise ScanError(
                f"File limit exceeded ({max_files}). Narrow the repository or raise --max-files."
            )

    return files, source, symlinks_skipped, generated_skipped, requested_skipped


def is_env_template(name: str) -> bool:
    return name.endswith(ENV_TEMPLATE_SUFFIXES) or name in {
        ".env.example",
        ".env.sample",
        ".env.template",
    }


def is_secret_like_path(relative: Path) -> bool:
    name = relative.name.lower()
    if name == ".env" or (name.startswith(".env.") and not is_env_template(name)):
        return True
    if name in SECRET_FILENAMES or relative.suffix.lower() in SECRET_SUFFIXES:
        return True
    return any(
        token in name
        for token in ("credentials", "private-key", "private_key", "secret-token")
    )


def is_raw_conversation_path(relative: Path) -> bool:
    name = relative.name.lower()
    if relative.suffix.lower() not in {".html", ".json", ".txt", ".zip"}:
        return False
    return any(token in name for token in ("chat-export", "conversation", "transcript"))


def is_memory_path(relative: Path) -> bool:
    value = relative.as_posix().lower()
    return value.startswith(
        ("project-os/audit/", "project-os/discovery/", "project-os/safety/")
    ) and not value.endswith("/readme.md")


def is_agent_path(relative: Path) -> bool:
    name = relative.name.lower()
    return name in AGENT_FILENAMES or relative.as_posix().lower().endswith(
        ".github/copilot-instructions.md"
    )


def looks_like_placeholder(value: str) -> bool:
    normalized = value.strip("\"'<>[]{}() ").lower()
    if not normalized:
        return True
    if normalized in PLACEHOLDER_MARKERS:
        return True
    if any(marker in normalized for marker in PLACEHOLDER_MARKERS):
        return True
    if normalized.startswith(
        (
            "${",
            "$",
            "env.",
            "process.env",
            "os.environ",
            "context.env",
            "ctx.env",
            "import.meta.env",
        )
    ):
        return True
    if set(normalized) <= {"x", "*", "-", "_"}:
        return True
    return False


def looks_like_path_placeholder(value: str) -> bool:
    normalized = value.lower()
    return any(
        marker in normalized
        for marker in ("...", "<", ">", "{user}", "[^", r"\s", "example", "sample")
    )


def disposition(rule_id: str, profile: str) -> str:
    if rule_id in {"SAF001", "SAF002", "SAF003", "SAF004", "SAF005", "SAF007"}:
        return "review" if profile == "local" else "block"
    if rule_id == "SAF006":
        return {
            "local": "info",
            "private": "info",
            "team": "review",
            "public": "block",
        }[profile]
    if rule_id == "SAF008":
        return "info" if profile in {"local", "private"} else "review"
    if rule_id == "SAF009":
        return "review" if profile == "public" else "info"
    return "review"


def severity(rule_id: str) -> str:
    if rule_id in {"SAF002", "SAF003", "SAF005"}:
        return "critical"
    if rule_id in {"SAF001", "SAF004", "SAF007"}:
        return "high"
    if rule_id == "SAF006":
        return "medium"
    return "low"


def classification(rule_id: str) -> str:
    if rule_id in {"SAF001", "SAF002", "SAF003", "SAF004", "SAF005", "SAF007"}:
        return "Local Only"
    if rule_id in {"SAF006", "SAF008"}:
        return "Private Repo"
    if rule_id == "SAF009":
        return "Team Shared"
    return "Unknown"


def finding(rule_id: str, relative: Path, profile: str) -> dict[str, str]:
    return {
        "rule_id": rule_id,
        "path": relative.as_posix(),
        "severity": severity(rule_id),
        "classification": classification(rule_id),
        "disposition": disposition(rule_id, profile),
        "remediation": REMEDIATION[rule_id],
    }


def path_rule_ids(relative: Path) -> list[str]:
    rules: list[str] = []
    if is_secret_like_path(relative):
        rules.append("SAF001")
    if is_raw_conversation_path(relative):
        rules.append("SAF007")
    if is_memory_path(relative):
        rules.append("SAF008")
    if is_agent_path(relative):
        rules.append("SAF009")
    return rules


def text_rule_ids(text: str) -> list[str]:
    rules: list[str] = []
    if PRIVATE_KEY_RE.search(text):
        rules.append("SAF002")
    if any(pattern.search(text) for pattern in PROVIDER_TOKEN_RES):
        rules.append("SAF003")

    assignments = CREDENTIAL_ASSIGNMENT_RE.findall(text)
    if any(not looks_like_placeholder(value) for value in assignments):
        rules.append("SAF004")
    if CONNECTION_STRING_RE.search(text):
        rules.append("SAF005")
    absolute_paths = ABSOLUTE_USER_PATH_RE.findall(text)
    if any(not looks_like_path_placeholder(value) for value in absolute_paths):
        rules.append("SAF006")
    return rules


def read_safe_text(path: Path, max_bytes: int) -> tuple[str | None, str | None]:
    try:
        size = path.stat().st_size
    except OSError:
        return None, "unreadable"
    if size > max_bytes:
        return None, "large"
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name.lower() not in {
        ".env",
        ".npmrc",
        ".pypirc",
        "dockerfile",
        "makefile",
    }:
        return None, "unsupported"
    try:
        data = path.read_bytes()
    except OSError:
        return None, "unreadable"
    if b"\x00" in data:
        return None, "binary"
    return data.decode("utf-8", errors="replace"), None


def scan_repository(
    root: Path,
    profile: str,
    scope: str,
    output_relative: Path,
    max_files: int,
    max_bytes: int,
    exclude_prefixes: Iterable[str] = (),
) -> dict[str, Any]:
    normalized_exclusions = normalize_exclude_prefixes(exclude_prefixes)
    files, source, symlinks_skipped, generated_skipped, requested_skipped = list_scope_files(
        root, scope, output_relative, max_files, normalized_exclusions
    )
    tracked = git_paths(root, "ls-files", "-z") if is_git_repository(root) else set()
    staged = (
        git_paths(root, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
        if is_git_repository(root)
        else set()
    )

    raw_findings: list[dict[str, Any]] = []
    skipped = {"binary": 0, "large": 0, "unreadable": 0, "unsupported": 0}
    files_scanned = 0

    for relative in files:
        rules = path_rule_ids(relative)
        text, reason = read_safe_text(root / relative, max_bytes)
        if text is not None:
            files_scanned += 1
            rules.extend(text_rule_ids(text))
        elif reason:
            skipped[reason] += 1

        for rule_id in sorted(set(rules)):
            item: dict[str, Any] = finding(rule_id, relative, profile)
            item["tracked"] = relative.as_posix() in tracked
            item["staged"] = relative.as_posix() in staged
            raw_findings.append(item)

    raw_findings.sort(key=lambda item: (item["path"], item["rule_id"]))
    findings: list[dict[str, Any]] = []
    for index, item in enumerate(raw_findings, start=1):
        findings.append({"finding_id": f"SAF-{index:04d}", **item})

    counts = {
        name: sum(1 for item in findings if item["disposition"] == name)
        for name in ("block", "review", "info")
    }
    gate_result = "Block" if counts["block"] else "Review" if counts["review"] else "Go"

    commit = None
    if is_git_repository(root):
        result = run_git(root, "rev-parse", "HEAD")
        if result.returncode == 0:
            commit = result.stdout.strip() or None

    return {
        "schema_version": SCHEMA_VERSION,
        "scanner": "AI Project OS safety_scan.py",
        "profile": profile,
        "scope": scope,
        "root": ".",
        "source": source,
        "commit": commit,
        "safety": {
            "read_only_by_default": True,
            "matched_values_emitted": False,
            "source_lines_emitted": False,
            "environment_values_emitted": False,
            "file_contents_emitted": False,
            "report_paths_are_repository_relative": True,
        },
        "summary": {
            "files_considered": len(files),
            "files_scanned": files_scanned,
            "block_findings": counts["block"],
            "review_findings": counts["review"],
            "info_findings": counts["info"],
            "gate_result": gate_result,
        },
        "findings": findings,
        "skipped": {
            **skipped,
            "symlinks": symlinks_skipped,
            "generated_or_vendor": generated_skipped,
            "requested_prefixes": requested_skipped,
        },
        "excluded_prefixes": list(normalized_exclusions),
    }


def resolve_output(root: Path, output_dir: str) -> tuple[Path, Path]:
    root = root.resolve()
    candidate = Path(output_dir)
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ScanError("Output directory must be inside the repository root.") from exc
    output_path = resolved / OUTPUT_NAME
    return output_path, output_path.relative_to(root)


def rendered_json(evidence: dict[str, Any]) -> str:
    return json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.replace(path)


def print_summary(evidence: dict[str, Any]) -> None:
    summary = evidence["summary"]
    print("AI Project OS Safety Scan / AI Project OS 安全扫描")
    print(f"Profile / Profile: {evidence['profile']}")
    print(f"Scope / 范围: {evidence['scope']}")
    print(f"Files considered / 文件数: {summary['files_considered']}")
    print(f"Block / 阻塞: {summary['block_findings']}")
    print(f"Review / 复核: {summary['review_findings']}")
    print(f"Info / 信息: {summary['info_findings']}")
    print(f"Gate / 门禁: {summary['gate_result']}")
    print("Matched values emitted / 输出命中值: No / 否")
    print("Source lines emitted / 输出命中行: No / 否")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect sanitized AI Project OS repository-safety evidence."
    )
    parser.add_argument("--root", default=".", help="Repository root. Defaults to cwd.")
    parser.add_argument("--profile", choices=PROFILES, default="local")
    parser.add_argument("--scope", choices=SCOPES, default="worktree")
    parser.add_argument(
        "--output-dir",
        default="project-os/safety",
        help="Repository-internal output directory used by --write/--check.",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", action="store_true", help="Write SAFETY_EVIDENCE.json.")
    action.add_argument("--check", action="store_true", help="Check existing evidence.")
    parser.add_argument("--summary", action="store_true", help="Print a sanitized summary.")
    parser.add_argument(
        "--fail-on-block",
        action="store_true",
        help="Exit 2 when the selected profile has Block findings.",
    )
    parser.add_argument("--max-files", type=int, default=50_000)
    parser.add_argument("--max-bytes", type=int, default=MAX_FILE_BYTES)
    parser.add_argument(
        "--exclude-prefix",
        action="append",
        default=[],
        help="Repository-relative path prefix to exclude; repeat as needed.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print("Root must be an existing directory.", file=sys.stderr)
        return 1
    if args.max_files < 1 or args.max_bytes < 1:
        print("File and byte limits must be positive.", file=sys.stderr)
        return 1

    try:
        output_path, output_relative = resolve_output(root, args.output_dir)
        evidence = scan_repository(
            root,
            args.profile,
            args.scope,
            output_relative,
            args.max_files,
            args.max_bytes,
            args.exclude_prefix,
        )
    except ScanError as exc:
        print(f"Safety scan stopped: {exc}", file=sys.stderr)
        return 1

    content = rendered_json(evidence)
    if args.write:
        write_atomic(output_path, content)
        print(output_path.relative_to(root).as_posix())
    elif args.check:
        if not output_path.exists():
            print(f"Missing evidence: {output_path.relative_to(root)}", file=sys.stderr)
            return 1
        if output_path.read_text(encoding="utf-8") != content:
            print(f"Stale evidence: {output_path.relative_to(root)}", file=sys.stderr)
            return 1
        print(f"Current evidence: {output_path.relative_to(root)}")
    elif args.summary:
        print_summary(evidence)
    else:
        print(content, end="")

    if args.fail_on_block and evidence["summary"]["block_findings"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
