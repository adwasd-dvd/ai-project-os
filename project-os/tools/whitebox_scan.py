#!/usr/bin/env python3
"""Collect deterministic, path-only evidence for AI Project OS whiteboxing.

The scanner is read-only unless --write is provided. Even in write mode it only
writes SCAN_EVIDENCE.json under a caller-selected directory inside the scanned
repository. It never emits environment-variable values or secret-file contents.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlsplit, urlunsplit

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11+ is expected
    tomllib = None


SCHEMA_VERSION = "1.0"
OUTPUT_NAME = "SCAN_EVIDENCE.json"

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "__pycache__",
    "bower_components",
    "coverage",
    "dist",
    "build",
    "node_modules",
    "target",
    "vendor",
}

LANGUAGE_SUFFIXES = {
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".cs": "C#",
    ".css": "CSS",
    ".dart": "Dart",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".go": "Go",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".html": "HTML",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "JavaScript JSX",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".lua": "Lua",
    ".m": "Objective-C",
    ".php": "PHP",
    ".pl": "Perl",
    ".py": "Python",
    ".r": "R",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".scala": "Scala",
    ".sh": "Shell",
    ".sql": "SQL",
    ".swift": "Swift",
    ".ts": "TypeScript",
    ".tsx": "TypeScript TSX",
    ".vue": "Vue",
}

MANIFEST_NAMES = {
    "package.json": "npm",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "setup.py": "python",
    "setup.cfg": "python",
    "pipfile": "python",
    "poetry.lock": "python-lock",
    "cargo.toml": "rust",
    "go.mod": "go",
    "composer.json": "php",
    "gemfile": "ruby",
    "mix.exs": "elixir",
    "pom.xml": "maven",
    "build.gradle": "gradle",
    "build.gradle.kts": "gradle",
    "pubspec.yaml": "dart",
}

LOCKFILE_NAMES = {
    "package-lock.json",
    "npm-shrinkwrap.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "bun.lock",
    "bun.lockb",
    "poetry.lock",
    "pipfile.lock",
    "uv.lock",
    "cargo.lock",
    "go.sum",
    "composer.lock",
    "gemfile.lock",
    "mix.lock",
    "gradle.lockfile",
    "pubspec.lock",
}

DOC_SUFFIXES = {".md", ".mdx", ".rst", ".adoc", ".txt"}
CONFIG_SUFFIXES = {".yaml", ".yml", ".toml", ".ini", ".conf", ".properties"}
ENV_TEMPLATE_SUFFIXES = (".example", ".sample", ".template")
ENTRYPOINT_NAMES = {
    "__main__.py",
    "app.py",
    "main.py",
    "manage.py",
    "server.py",
    "cli.py",
    "index.js",
    "index.ts",
    "main.js",
    "main.ts",
    "server.js",
    "server.ts",
    "app.js",
    "app.ts",
    "dockerfile",
    "procfile",
}
INFRA_NAMES = {
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "compose.yml",
    "compose.yaml",
    "procfile",
    "vercel.json",
    "netlify.toml",
    "fly.toml",
    "render.yaml",
}
SECRET_NAME_TOKENS = {"secret", "credential", "credentials", "private_key", "token"}


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


def git_value(root: Path, *args: str) -> str | None:
    result = run_git(root, *args)
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def sanitize_remote(remote: str) -> str:
    """Remove credentials and local absolute paths from a Git remote."""

    if "://" in remote:
        parsed = urlsplit(remote)
        hostname = parsed.hostname or ""
        if parsed.port:
            hostname = f"{hostname}:{parsed.port}"
        return urlunsplit((parsed.scheme, hostname, parsed.path, "", ""))
    if re.match(r"^[^/@\s]+@[^:\s]+:", remote):
        return remote.split("@", 1)[1]
    if remote.startswith(("/", "./", "../", "~")):
        return "<local-path>"
    return remote


def git_info(root: Path) -> dict[str, Any]:
    is_repo = git_value(root, "rev-parse", "--is-inside-work-tree") == "true"
    if not is_repo:
        return {"is_repository": False}

    remotes: list[dict[str, str]] = []
    remote_names = git_value(root, "remote")
    for name in sorted((remote_names or "").splitlines()):
        url = git_value(root, "remote", "get-url", name)
        if url:
            remotes.append({"name": name, "url": sanitize_remote(url)})

    return {
        "is_repository": True,
        "branch": git_value(root, "branch", "--show-current"),
        "commit": git_value(root, "rev-parse", "HEAD"),
        "latest_tag": git_value(root, "describe", "--tags", "--abbrev=0"),
        "remotes": remotes,
    }


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


def list_repository_files(
    root: Path,
    output_relative: Path,
    max_files: int,
    exclude_prefixes: tuple[str, ...] = (),
) -> tuple[list[Path], str, int, int, list[str]]:
    """Return safe relative file paths, source, generated exclusions, symlinks."""

    result = run_git(root, "ls-files", "-co", "--exclude-standard", "-z")
    source = "git ls-files"
    raw_paths: Iterable[str]
    if result.returncode == 0:
        raw_paths = result.stdout.split("\0")
    else:
        source = "filesystem fallback"
        walked: list[str] = []
        for current, dirs, files in os.walk(root, followlinks=False):
            dirs[:] = sorted(directory for directory in dirs if directory.lower() not in SKIP_DIRS)
            current_path = Path(current)
            for filename in sorted(files):
                walked.append((current_path / filename).relative_to(root).as_posix())
        raw_paths = walked

    files: list[Path] = []
    symlinks: list[str] = []
    excluded_generated = 0
    excluded_requested = 0
    for raw in raw_paths:
        if not raw:
            continue
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            continue
        if relative == output_relative:
            continue
        if excluded_by_prefix(relative, exclude_prefixes):
            excluded_requested += 1
            continue
        if should_skip(relative):
            excluded_generated += 1
            continue
        absolute = root / relative
        if absolute.is_symlink():
            symlinks.append(relative.as_posix())
            continue
        if not absolute.is_file():
            continue
        files.append(relative)

    files = sorted(set(files), key=lambda item: item.as_posix())
    if len(files) > max_files:
        raise ScanError(
            f"File limit exceeded: {len(files)} > {max_files}. "
            "Narrow the repository scope or raise --max-files explicitly."
        )
    return files, source, excluded_generated, excluded_requested, sorted(set(symlinks))


def is_test_path(path: Path) -> bool:
    lowered_parts = [part.lower() for part in path.parts]
    name = path.name.lower()
    return (
        any(part in {"test", "tests", "spec", "specs", "__tests__"} for part in lowered_parts)
        or name.startswith("test_")
        or name.endswith(("_test.py", ".test.js", ".test.ts", ".spec.js", ".spec.ts"))
    )


def is_ci_path(path: Path) -> bool:
    lowered = path.as_posix().lower()
    return (
        lowered.startswith(".github/workflows/")
        or lowered in {".gitlab-ci.yml", "azure-pipelines.yml", "bitbucket-pipelines.yml", "jenkinsfile"}
        or lowered.startswith(".circleci/")
    )


def is_config_path(path: Path) -> bool:
    lowered = path.as_posix().lower()
    name = path.name.lower()
    return (
        path.suffix.lower() in CONFIG_SUFFIXES
        or name.startswith(".env.")
        or name in {".envrc", "config.json", "settings.json", "tsconfig.json", "jsconfig.json"}
        or "/config/" in f"/{lowered}/"
    )


def is_data_path(path: Path) -> bool:
    lowered_parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    return bool(
        lowered_parts
        & {
            "data",
            "db",
            "database",
            "fixtures",
            "migrations",
            "models",
            "schema",
            "schemas",
            "seeds",
        }
    ) or any(token in name for token in ("schema", "migration", "fixture", "seed"))


def is_infrastructure_path(path: Path) -> bool:
    lowered = path.as_posix().lower()
    return (
        path.name.lower() in INFRA_NAMES
        or path.suffix.lower() == ".tf"
        or any(token in lowered.split("/") for token in ("helm", "k8s", "kubernetes", "terraform"))
    )


def is_secret_like(path: Path) -> bool:
    name = path.name.lower()
    if name == ".env" or (name.startswith(".env.") and not name.endswith(ENV_TEMPLATE_SUFFIXES)):
        return True
    if name in {"id_rsa", "id_dsa", "id_ed25519", ".npmrc", ".pypirc"}:
        return True
    if path.suffix.lower() in {".key", ".pem", ".p12", ".pfx", ".jks"}:
        return True
    stem = path.stem.lower()
    return any(token in stem for token in SECRET_NAME_TOKENS)


def is_env_template(path: Path) -> bool:
    name = path.name.lower()
    return name.startswith(".env") and name.endswith(ENV_TEMPLATE_SUFFIXES)


def read_env_key_names(path: Path) -> list[str]:
    keys: set[str] = set()
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("export "):
                stripped = stripped[7:].lstrip()
            candidate = stripped.split("=", 1)[0].strip()
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", candidate):
                keys.add(candidate)
    except OSError:
        return []
    return sorted(keys)


def safe_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def safe_toml(path: Path) -> dict[str, Any] | None:
    if tomllib is None:
        return None
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError):
        return None
    return value if isinstance(value, dict) else None


def add_dependency_rows(
    rows: set[tuple[str, str, str]], manifest: Path, root: Path
) -> None:
    """Extract dependency names and scopes, never versions or source URLs."""

    name = manifest.name.lower()
    rel = manifest.relative_to(root).as_posix()

    if name == "package.json":
        data = safe_json(manifest) or {}
        for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            values = data.get(section, {})
            if isinstance(values, dict):
                for dependency in values:
                    rows.add((rel, section, str(dependency)))
        return

    if name == "composer.json":
        data = safe_json(manifest) or {}
        for section in ("require", "require-dev"):
            values = data.get(section, {})
            if isinstance(values, dict):
                for dependency in values:
                    rows.add((rel, section, str(dependency)))
        return

    if name in {"pyproject.toml", "cargo.toml"}:
        data = safe_toml(manifest) or {}
        if name == "pyproject.toml":
            project = data.get("project", {})
            if isinstance(project, dict):
                dependencies = project.get("dependencies", [])
                if isinstance(dependencies, list):
                    for declaration in dependencies:
                        dependency = re.split(r"[\s<>=!~\[]", str(declaration), maxsplit=1)[0]
                        if dependency:
                            rows.add((rel, "project.dependencies", dependency))
                optional = project.get("optional-dependencies", {})
                if isinstance(optional, dict):
                    for group, declarations in optional.items():
                        if isinstance(declarations, list):
                            for declaration in declarations:
                                dependency = re.split(r"[\s<>=!~\[]", str(declaration), maxsplit=1)[0]
                                if dependency:
                                    rows.add((rel, f"optional:{group}", dependency))
            poetry = data.get("tool", {}).get("poetry", {}) if isinstance(data.get("tool"), dict) else {}
            if isinstance(poetry, dict):
                for section in ("dependencies", "dev-dependencies"):
                    values = poetry.get(section, {})
                    if isinstance(values, dict):
                        for dependency in values:
                            if str(dependency).lower() != "python":
                                rows.add((rel, f"poetry.{section}", str(dependency)))
        else:
            for section in ("dependencies", "dev-dependencies", "build-dependencies"):
                values = data.get(section, {})
                if isinstance(values, dict):
                    for dependency in values:
                        rows.add((rel, section, str(dependency)))
        return

    if name == "go.mod":
        try:
            lines = manifest.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return
        in_require = False
        for line in lines:
            stripped = line.strip()
            if stripped == "require (":
                in_require = True
                continue
            if in_require and stripped == ")":
                in_require = False
                continue
            if stripped.startswith("require "):
                parts = stripped.split()
                if len(parts) >= 2:
                    rows.add((rel, "require", parts[1]))
            elif in_require and stripped and not stripped.startswith("//"):
                parts = stripped.split()
                if parts:
                    rows.add((rel, "require", parts[0]))
        return

    if name == "requirements.txt":
        try:
            lines = manifest.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "-")) or "://" in stripped or " @ " in stripped:
                continue
            dependency = re.split(r"[\s<>=!~\[]", stripped, maxsplit=1)[0]
            if re.fullmatch(r"[A-Za-z0-9_.-]+", dependency):
                rows.add((rel, "requirement", dependency))


def limited(items: Iterable[Any], max_items: int) -> dict[str, Any]:
    values = list(items)
    return {"items": values[:max_items], "omitted": max(0, len(values) - max_items)}


def build_evidence(
    root: Path,
    output_dir: Path,
    max_files: int = 100_000,
    max_items: int = 500,
    large_file_bytes: int = 5 * 1024 * 1024,
    exclude_prefixes: Iterable[str] = (),
) -> dict[str, Any]:
    root = root.resolve()
    output_dir = output_dir.resolve()
    try:
        output_relative = (output_dir / OUTPUT_NAME).relative_to(root)
    except ValueError as exc:
        raise ScanError("Output directory must be inside the repository root.") from exc

    normalized_exclusions = normalize_exclude_prefixes(exclude_prefixes)
    files, file_source, excluded_generated, excluded_requested, symlinks = list_repository_files(
        root, output_relative, max_files, normalized_exclusions
    )

    languages: Counter[str] = Counter()
    manifests: list[dict[str, str]] = []
    lockfiles: list[str] = []
    documents: list[str] = []
    configs: list[str] = []
    data_paths: list[str] = []
    tests: list[str] = []
    entrypoints: list[str] = []
    ci_paths: list[str] = []
    infrastructure: list[str] = []
    secret_like_paths: list[str] = []
    environment_keys: list[dict[str, str]] = []
    large_files: list[dict[str, Any]] = []
    dependency_rows: set[tuple[str, str, str]] = set()
    total_bytes = 0

    for relative in files:
        absolute = root / relative
        rel = relative.as_posix()
        try:
            size = absolute.stat().st_size
        except OSError:
            continue
        total_bytes += size
        if size >= large_file_bytes:
            large_files.append({"path": rel, "size_bytes": size})

        language = LANGUAGE_SUFFIXES.get(relative.suffix.lower())
        if language:
            languages[language] += 1

        basename = relative.name.lower()
        if basename in MANIFEST_NAMES:
            manifests.append({"path": rel, "ecosystem": MANIFEST_NAMES[basename]})
            add_dependency_rows(dependency_rows, absolute, root)
        if basename in LOCKFILE_NAMES:
            lockfiles.append(rel)
        if relative.suffix.lower() in DOC_SUFFIXES or basename.startswith("readme"):
            documents.append(rel)
        if is_config_path(relative):
            configs.append(rel)
        if is_data_path(relative):
            data_paths.append(rel)
        if is_test_path(relative):
            tests.append(rel)
        if basename in ENTRYPOINT_NAMES:
            entrypoints.append(rel)
        if is_ci_path(relative):
            ci_paths.append(rel)
        if is_infrastructure_path(relative):
            infrastructure.append(rel)
        if is_secret_like(relative):
            secret_like_paths.append(rel)
        if is_env_template(relative):
            for key in read_env_key_names(absolute):
                environment_keys.append({"key": key, "source": rel})

    language_rows = [
        {"language": language, "file_count": count}
        for language, count in sorted(languages.items(), key=lambda item: (-item[1], item[0]))
    ]
    dependencies = [
        {"manifest": manifest, "scope": scope, "name": name}
        for manifest, scope, name in sorted(dependency_rows)
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "scanner": "AI Project OS whitebox_scan v0.4",
        "safety": {
            "mode": "path-and-declaration metadata only",
            "secret_values_emitted": False,
            "environment_values_emitted": False,
            "file_contents_emitted": False,
        },
        "repository": {
            "name": root.name,
            "git": git_info(root),
            "file_source": file_source,
        },
        "coverage": {
            "file_count": len(files),
            "total_bytes": total_bytes,
            "excluded_common_generated_count": excluded_generated,
            "excluded_requested_count": excluded_requested,
            "excluded_prefixes": list(normalized_exclusions),
            "symlink_count": len(symlinks),
            "max_files": max_files,
            "max_items_per_category": max_items,
        },
        "languages": language_rows,
        "manifests": limited(sorted(manifests, key=lambda item: item["path"]), max_items),
        "lockfiles": limited(sorted(set(lockfiles)), max_items),
        "dependency_declarations": limited(dependencies, max_items),
        "likely_entrypoints": limited(sorted(set(entrypoints)), max_items),
        "tests": limited(sorted(set(tests)), max_items),
        "documents": limited(sorted(set(documents)), max_items),
        "configuration_candidates": limited(sorted(set(configs)), max_items),
        "data_and_schema_candidates": limited(sorted(set(data_paths)), max_items),
        "ci_candidates": limited(sorted(set(ci_paths)), max_items),
        "infrastructure_candidates": limited(sorted(set(infrastructure)), max_items),
        "environment_key_names": limited(
            sorted(environment_keys, key=lambda item: (item["source"], item["key"])), max_items
        ),
        "secret_like_paths": limited(sorted(set(secret_like_paths)), max_items),
        "symlink_paths_not_followed": limited(symlinks, max_items),
        "large_files": limited(sorted(large_files, key=lambda item: item["path"]), max_items),
    }


def render_json(evidence: dict[str, Any]) -> str:
    return json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def resolve_output_dir(root: Path, requested: str) -> Path:
    candidate = (root / requested).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ScanError("Output directory must be inside the repository root.") from exc
    return candidate


def write_evidence(output_dir: Path, rendered: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / OUTPUT_NAME
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=output_dir,
        prefix=f".{OUTPUT_NAME}.",
        delete=False,
    ) as handle:
        handle.write(rendered)
        temp_path = Path(handle.name)
    os.replace(temp_path, output_path)
    return output_path


def print_summary(evidence: dict[str, Any], output: Path | None = None) -> None:
    coverage = evidence["coverage"]
    print("AI Project OS Whitebox Scan / AI Project OS 白盒扫描")
    print(f"Files / 文件: {coverage['file_count']}")
    print(f"Manifests / Manifest: {len(evidence['manifests']['items'])}")
    print(f"Documents / 文档: {len(evidence['documents']['items'])}")
    print(f"Tests / 测试: {len(evidence['tests']['items'])}")
    print(f"Secret-like paths / 疑似敏感路径: {len(evidence['secret_like_paths']['items'])}")
    print("Secret values emitted / 输出 secret 值: No / 否")
    if output:
        print(f"Written / 已写入: {output}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect deterministic, read-only whitebox evidence."
    )
    parser.add_argument("--root", default=".", help="Repository root. Defaults to cwd.")
    parser.add_argument(
        "--output-dir",
        default="project-os/discovery",
        help="Output directory relative to root. Must stay inside root.",
    )
    parser.add_argument("--write", action="store_true", help="Write SCAN_EVIDENCE.json.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the existing SCAN_EVIDENCE.json is missing or stale.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a compact summary instead of JSON in dry-run mode.",
    )
    parser.add_argument("--max-files", type=int, default=100_000)
    parser.add_argument("--max-items", type=int, default=500)
    parser.add_argument("--large-file-mb", type=int, default=5)
    parser.add_argument(
        "--exclude-prefix",
        action="append",
        default=[],
        help="Repository-relative path prefix to exclude; repeat as needed.",
    )
    args = parser.parse_args()

    if args.write and args.check:
        parser.error("--write and --check cannot be used together")
    if args.max_files <= 0 or args.max_items <= 0 or args.large_file_mb <= 0:
        parser.error("limits must be positive integers")

    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error(f"repository root does not exist: {root}")

    try:
        output_dir = resolve_output_dir(root, args.output_dir)
        evidence = build_evidence(
            root,
            output_dir,
            max_files=args.max_files,
            max_items=args.max_items,
            large_file_bytes=args.large_file_mb * 1024 * 1024,
            exclude_prefixes=args.exclude_prefix,
        )
        rendered = render_json(evidence)
    except ScanError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 2

    output_path = output_dir / OUTPUT_NAME
    if args.check:
        if not output_path.exists():
            print(f"[FAIL] Missing evidence / 缺少证据: {output_path}")
            return 1
        try:
            existing = output_path.read_text(encoding="utf-8")
        except OSError as exc:
            print(f"[FAIL] Cannot read evidence / 无法读取证据: {exc}")
            return 1
        if existing != rendered:
            print(f"[FAIL] Evidence is stale / 证据已过期: {output_path}")
            return 1
        print(f"[PASS] Evidence is current / 证据为最新: {output_path}")
        return 0

    if args.write:
        written = write_evidence(output_dir, rendered)
        print_summary(evidence, written.relative_to(root))
        return 0

    if args.summary:
        print_summary(evidence)
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
