#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import subprocess
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".sh",
    ".ps1",
    ".cmd",
    ".crt",
    ".mobileconfig",
    ".yml",
    ".yaml",
    ".json",
    ".py",
}

FORBIDDEN_PATTERNS = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\b(?:10|127)\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"), "RFC1918 or loopback IPv4 address"),
    (re.compile(r"\b192\.168\.\d{1,3}\.\d{1,3}\b"), "RFC1918 IPv4 address"),
    (re.compile(r"\b172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}\b"), "RFC1918 IPv4 address"),
    (re.compile(r"\b[a-z0-9-]+(?:\.[a-z0-9-]+)*\.home\.arpa\b", re.IGNORECASE), "private hostname"),
    (re.compile(r"/Users/"), "local workstation path"),
    (re.compile(r"\b(?:token|password|api[_ -]?key|secret)\b\s*[:=]\s*\S+", re.IGNORECASE), "credential-like assignment"),
]

FORBIDDEN_PATH_SUFFIXES = {".p12", ".pfx", ".key", ".key.pem", ".password", ".password.txt", ".secret"}


def tracked_files() -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line]


def is_text_candidate(path: pathlib.Path) -> bool:
    suffixes = "".join(path.suffixes[-2:]) if len(path.suffixes) >= 2 else path.suffix
    return path.suffix in TEXT_EXTENSIONS or suffixes in FORBIDDEN_PATH_SUFFIXES


def main() -> int:
    failures: list[str] = []

    for path in tracked_files():
        rel = path.relative_to(REPO_ROOT)
        suffixes = "".join(path.suffixes[-2:]) if len(path.suffixes) >= 2 else path.suffix
        if path.suffix in FORBIDDEN_PATH_SUFFIXES or suffixes in FORBIDDEN_PATH_SUFFIXES:
            failures.append(f"{rel}: forbidden sensitive file type")
            continue

        if not is_text_candidate(path):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"{rel}: expected text file is not valid UTF-8")
            continue

        for pattern, reason in FORBIDDEN_PATTERNS:
            if rel == pathlib.Path("scripts/public_scope_guard.py") and reason in {
                "local workstation path",
                "credential-like assignment",
                "private hostname",
                "RFC1918 or loopback IPv4 address",
                "RFC1918 IPv4 address",
            }:
                continue
            if pattern.search(text):
                failures.append(f"{rel}: contains {reason}")

    if failures:
        print("Public scope guard failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("Public scope guard passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
