#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
CERT_SOURCE="${REPO_ROOT}/certs/doop-root-ca.crt"
CERT_TARGET="/etc/pki/ca-trust/source/anchors/doop-root-ca.crt"

if [[ ! -f "${CERT_SOURCE}" ]]; then
  echo "Root certificate not found at ${CERT_SOURCE}" >&2
  exit 1
fi

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root." >&2
  exit 1
fi

install -m 0644 "${CERT_SOURCE}" "${CERT_TARGET}"
update-ca-trust extract

echo "Installed doop root CA into the RHEL/Fedora trust store."
