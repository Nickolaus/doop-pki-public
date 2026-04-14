#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import pathlib
import plistlib
import re
import subprocess
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
CERT_PATH = REPO_ROOT / "certs" / "doop-root-ca.crt"
README_PATH = REPO_ROOT / "README.md"
MOBILECONFIG_PATH = REPO_ROOT / "apple" / "doop-root-ca.mobileconfig"

EXPECTED_CERT_REL = "certs/doop-root-ca.crt"


def run(*args: str) -> str:
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def main() -> int:
    failures: list[str] = []

    cert_der = subprocess.run(
        ["openssl", "x509", "-in", str(CERT_PATH), "-outform", "der"],
        check=True,
        capture_output=True,
    ).stdout
    cert_sha = hashlib.sha256(cert_der).hexdigest().upper()
    openssl_subject = run("openssl", "x509", "-in", str(CERT_PATH), "-noout", "-subject")
    openssl_fingerprint = run("openssl", "x509", "-in", str(CERT_PATH), "-noout", "-fingerprint", "-sha256")
    openssl_enddate = run("openssl", "x509", "-in", str(CERT_PATH), "-noout", "-enddate")

    readme = README_PATH.read_text(encoding="utf-8")
    if EXPECTED_CERT_REL not in readme:
        failures.append(f"README.md: missing canonical artifact path {EXPECTED_CERT_REL}")

    fingerprint_match = re.search(r"SHA-256 fingerprint:\s*`([^`]+)`", readme)
    if not fingerprint_match:
        failures.append("README.md: missing SHA-256 fingerprint block")
    else:
        documented = fingerprint_match.group(1).replace(":", "").upper()
        actual = openssl_fingerprint.split("=", 1)[1].replace(":", "").upper()
        if documented != actual:
            failures.append("README.md: fingerprint does not match certs/doop-root-ca.crt")

    subject_match = re.search(r"Subject:\s*`([^`]+)`", readme)
    if not subject_match:
        failures.append("README.md: missing subject block")
    else:
        documented_subject = subject_match.group(1).strip()
        actual_subject = openssl_subject.split("subject=", 1)[1].strip()
        if documented_subject != actual_subject:
            failures.append("README.md: subject does not match certs/doop-root-ca.crt")

    validity_match = re.search(r"Valid until:\s*`([^`]+)`", readme)
    if not validity_match:
        failures.append("README.md: missing validity block")
    else:
        actual_enddate = openssl_enddate.split("=", 1)[1].strip()
        if validity_match.group(1).strip() != actual_enddate:
            failures.append("README.md: validity does not match certs/doop-root-ca.crt")

    with MOBILECONFIG_PATH.open("rb") as fh:
        mobileconfig = plistlib.load(fh)
    embedded_der = mobileconfig["PayloadContent"][0]["PayloadContent"]
    embedded_sha = hashlib.sha256(embedded_der).hexdigest().upper()
    if embedded_sha != cert_sha:
        failures.append("apple/doop-root-ca.mobileconfig: embedded certificate does not match certs/doop-root-ca.crt")

    for path in REPO_ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        if "certs/doop-root-ca.crt" in text or path == README_PATH:
            continue
        # no-op; markdown docs are allowed to omit the canonical path

    if failures:
        print("Artifact consistency check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("Artifact consistency check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
