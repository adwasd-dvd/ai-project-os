#!/usr/bin/env python3
"""Build a deterministic AI Project OS release zip from committed Git content."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path


SOURCE_PATH = "template/project-os"
PACKAGE_ROOT = "project-os"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


class BuildError(RuntimeError):
    """A safe, user-facing release build failure."""


def run_git(root: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as exc:
        raise BuildError(f"Cannot run Git: {exc}") from exc
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise BuildError(message or f"Git command failed: {' '.join(args)}")
    return result


def resolve_output(root: Path, value: str) -> Path:
    output = (root / value).resolve()
    releases = (root / "releases").resolve()
    try:
        output.relative_to(releases)
    except ValueError as exc:
        raise BuildError("Output must stay under the repository releases/ directory") from exc
    if output.suffix.lower() != ".zip":
        raise BuildError("Output must use the .zip extension")
    return output


def committed_source_tar(root: Path, treeish: str) -> bytes:
    dirty = run_git(
        root,
        ["status", "--porcelain", "--untracked-files=all", "--", SOURCE_PATH],
    ).stdout
    if dirty:
        raise BuildError(
            "Distributable template has uncommitted changes; commit them before packaging"
        )
    return run_git(
        root, ["archive", "--format=tar", treeish, SOURCE_PATH]
    ).stdout


def package_name(member_name: str) -> str:
    prefix = SOURCE_PATH + "/"
    if member_name == SOURCE_PATH:
        return PACKAGE_ROOT + "/"
    if not member_name.startswith(prefix):
        raise BuildError(f"Unexpected archive path: {member_name}")
    relative = member_name[len(prefix) :]
    return f"{PACKAGE_ROOT}/{relative}"


def zip_info(name: str, mode: int, is_dir: bool) -> zipfile.ZipInfo:
    normalized = name.rstrip("/") + "/" if is_dir else name
    info = zipfile.ZipInfo(normalized, FIXED_ZIP_TIME)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_STORED if is_dir else zipfile.ZIP_DEFLATED
    info.external_attr = ((0o40755 if is_dir else mode) & 0xFFFF) << 16
    if is_dir:
        info.external_attr |= 0x10
    return info


def build_release(root: Path, output_value: str, treeish: str = "HEAD") -> dict[str, object]:
    root = root.resolve()
    output = resolve_output(root, output_value)
    tar_bytes = committed_source_tar(root, treeish)
    output.parent.mkdir(parents=True, exist_ok=True)

    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=output.parent,
            prefix=".aipos-release-",
            suffix=".zip",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
        with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode="r:") as archive:
            members = sorted(archive.getmembers(), key=lambda item: item.name)
            with zipfile.ZipFile(
                temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9
            ) as bundle:
                seen: set[str] = set()
                for member in members:
                    if member.name == "template":
                        continue
                    name = package_name(member.name)
                    if name in seen:
                        raise BuildError(f"Duplicate archive path: {name}")
                    seen.add(name)
                    if member.isdir():
                        bundle.writestr(zip_info(name, 0o755, True), b"")
                        continue
                    if not member.isfile():
                        raise BuildError(f"Unsupported archive entry: {member.name}")
                    source = archive.extractfile(member)
                    if source is None:
                        raise BuildError(f"Cannot read archive entry: {member.name}")
                    mode = 0o755 if member.mode & 0o111 else 0o644
                    bundle.writestr(zip_info(name, mode, False), source.read())
        os.replace(temporary, output)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)

    data = output.read_bytes()
    return {
        "output": output.relative_to(root).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size": len(data),
        "treeish": treeish,
        "source": SOURCE_PATH,
        "package_root": PACKAGE_ROOT,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--output", required=True, help="Zip path under releases/")
    parser.add_argument("--treeish", default="HEAD", help="Committed Git treeish")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = build_release(Path(args.root), args.output, args.treeish)
    except BuildError as exc:
        print(f"[BLOCK] {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
