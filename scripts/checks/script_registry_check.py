#!/usr/bin/env python3
"""Validate script registry paths, syntax, and stale path references."""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys


SKIP_DIRS = {
    ".git",
    ".terraform",
    ".codex",
    "homelab",
    "doop-pki-public",
    "pki",
    "doop-local-artifacts",
    "logs",
    "node_modules",
    "__pycache__",
}
ARCHIVE_PARTS = {("docs", "archive")}
SCRIPT_SUFFIXES = {".py", ".sh"}
REQUIRED_FIELDS = {
    "id",
    "path",
    "owner",
    "language",
    "script_type",
    "safety",
    "public_interface",
    "called_by",
    "truth_source",
    "validation",
    "status",
}
VALID_LANGUAGES = {"bash", "python", "sh"}
VALID_SAFETY = {
    "read_only",
    "live_read_only",
    "local_mutation",
    "infrastructure_mutation",
    "secret_handling",
    "backup_restore",
}
VALID_STATUS = {"active", "deprecated", "archive"}
GENERIC_CALLERS = {
    "docs",
    "internal scripts",
    "GitHub Actions",
    "NixOS certbot services",
    "runtime config",
}


def parse_registry(path: pathlib.Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- id:"):
            current = {"id": line.split(":", 1)[1].strip().strip('"')}
            entries.append(current)
            continue
        if current is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"')
        if value and not value.startswith("{"):
            current[key.strip()] = value
    return entries


def run(cmd: list[str]) -> int:
    return subprocess.run(cmd, text=True).returncode


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not value.startswith("[") or not value.endswith("]"):
        return [value] if value else []
    return [item.strip().strip('"') for item in value[1:-1].split(",") if item.strip()]


def is_script_file(path: pathlib.Path) -> bool:
    if path.suffix in SCRIPT_SUFFIXES:
        return True
    try:
        with path.open("rb") as handle:
            return handle.read(2) == b"#!"
    except OSError:
        return False


def iter_text_files(root: pathlib.Path):
    for current_root, dirs, files in os.walk(root):
        rel_root = pathlib.Path(current_root).relative_to(root)
        dirs[:] = [
            d for d in dirs
            if d not in SKIP_DIRS and (tuple((rel_root / d).parts[:2]) not in ARCHIVE_PARTS)
        ]
        for name in files:
            path = pathlib.Path(current_root) / name
            if path.is_symlink() or path.stat().st_size > 2_000_000:
                continue
            yield path


def iter_script_candidates(root: pathlib.Path, registered_paths: set[pathlib.Path]):
    scan_roots = {root / "scripts"}
    for path in registered_paths:
        if path.exists() and not path.relative_to(root).parts[0] == "scripts":
            scan_roots.add(path.parent)
    for scan_root in sorted(scan_roots):
        if not scan_root.exists():
            continue
        for current_root, dirs, files in os.walk(scan_root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                path = pathlib.Path(current_root) / name
                if path.is_symlink() or path.suffix in {".pyc", ".md", ".yaml", ".yml"}:
                    continue
                if is_script_file(path):
                    yield path


def validate(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).resolve()
    registry = root / args.registry
    entries = parse_registry(registry)
    failures = 0

    if not entries:
        print(f"no registry entries found in {registry}", file=sys.stderr)
        return 1

    shell_paths: list[pathlib.Path] = []
    posix_paths: list[pathlib.Path] = []
    python_paths: list[pathlib.Path] = []
    old_paths: list[str] = []
    registered_paths: set[pathlib.Path] = set()
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()

    for entry in entries:
        missing_fields = sorted(REQUIRED_FIELDS - set(entry))
        if missing_fields:
            print(
                f"{entry.get('id', '<unknown>')}: missing fields: {', '.join(missing_fields)}",
                file=sys.stderr,
            )
            failures += len(missing_fields)
        entry_id = entry.get("id")
        if entry_id in seen_ids:
            print(f"{entry_id}: duplicate id", file=sys.stderr)
            failures += 1
        elif entry_id:
            seen_ids.add(entry_id)
        rel = entry.get("path")
        if not rel:
            print(f"{entry.get('id', '<unknown>')}: missing path", file=sys.stderr)
            failures += 1
            continue
        if rel in seen_paths:
            print(f"{entry.get('id')}: duplicate path {rel}", file=sys.stderr)
            failures += 1
        seen_paths.add(rel)
        path = root / rel
        if not path.exists():
            print(f"{entry.get('id')}: missing registered path {rel}", file=sys.stderr)
            failures += 1
            continue
        registered_paths.add(path.resolve())
        language = entry.get("language", "")
        if language == "bash":
            shell_paths.append(path)
        elif language == "sh":
            posix_paths.append(path)
        elif language == "python":
            python_paths.append(path)
        elif language:
            print(f"{entry.get('id')}: unsupported language {language}", file=sys.stderr)
            failures += 1
        if language and language not in VALID_LANGUAGES:
            print(f"{entry.get('id')}: invalid language {language}", file=sys.stderr)
            failures += 1
        safety = entry.get("safety")
        if safety and safety not in VALID_SAFETY:
            print(f"{entry.get('id')}: invalid safety {safety}", file=sys.stderr)
            failures += 1
        status = entry.get("status")
        if status and status not in VALID_STATUS:
            print(f"{entry.get('id')}: invalid status {status}", file=sys.stderr)
            failures += 1
        for caller in parse_inline_list(entry.get("called_by", "")):
            if caller in GENERIC_CALLERS or caller.startswith("mise run "):
                continue
            caller_path = root / caller
            if not caller_path.exists():
                print(f"{entry.get('id')}: called_by path does not exist: {caller}", file=sys.stderr)
                failures += 1
        old_path = entry.get("old_path")
        if old_path:
            old_paths.append(old_path)
            if (root / old_path).exists():
                print(f"{entry.get('id')}: old path still exists: {old_path}", file=sys.stderr)
                failures += 1

    unregistered = [
        path.relative_to(root).as_posix()
        for path in iter_script_candidates(root, registered_paths)
        if path.resolve() not in registered_paths
    ]
    if unregistered:
        failures += len(unregistered)
        for rel in sorted(unregistered):
            print(f"unregistered script: {rel}", file=sys.stderr)

    for path in shell_paths:
        failures += run(["bash", "-n", str(path)])
    for path in posix_paths:
        failures += run(["sh", "-n", str(path)])
    for path in python_paths:
        failures += run(["python3", "-m", "py_compile", str(path)])

    shellcheck = shutil.which("shellcheck")
    if shellcheck and shell_paths:
        failures += run([shellcheck, "-S", "error", *map(str, shell_paths)])
    elif shell_paths:
        print("warning: shellcheck not found; skipped shellcheck validation", file=sys.stderr)

    stale_hits: list[str] = []
    if old_paths:
        patterns = [(old, re.compile(re.escape(old))) for old in old_paths]
        for path in iter_text_files(root):
            rel = path.relative_to(root).as_posix()
            if rel == args.registry:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for old, pattern in patterns:
                if pattern.search(text):
                    stale_hits.append(f"{rel}: stale reference to {old}")
    if stale_hits:
        failures += len(stale_hits)
        print("\n".join(stale_hits), file=sys.stderr)

    if failures:
        print(f"script registry check failed: {failures}", file=sys.stderr)
        return 1
    print(f"script registry OK: {len(entries)} entries")
    return 0


def inventory(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).resolve()
    entries = parse_registry(root / args.registry)
    for entry in entries:
        print(
            f"{entry.get('id')}: {entry.get('safety')} {entry.get('language')} "
            f"{entry.get('path')} via {entry.get('public_interface')}"
        )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "inventory"])
    parser.add_argument("--root", default=".")
    parser.add_argument("--registry", default="scripts/registry.yaml")
    args = parser.parse_args()
    if args.command == "check":
        return validate(args)
    return inventory(args)


if __name__ == "__main__":
    raise SystemExit(main())
