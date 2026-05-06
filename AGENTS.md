# AGENTS.md

## Scope

`doop-pki-public/` is an independent public-safe repo for trust-distribution artifacts and generic client guidance.

Start with [`README.md`](./README.md), [`SECURITY.md`](./SECURITY.md), and [`docs/README.md`](./docs/README.md).

## Public-Safety Boundary

- This repo may contain the public root certificate, install scripts, platform notes, and public-safe troubleshooting guidance.
- Do not add private keys, passwords, tokens, internal service inventory, private hostnames, RFC1918 IPs, local workstation paths, or private topology.
- Do not copy content from `../pki/doop-internal-ca/` without a public-safety review.
- Keep docs generic enough for public publication.

## Source Of Truth

- Root certificate artifact: [`certs/doop-root-ca.crt`](./certs/doop-root-ca.crt).
- Apple profile artifact: [`apple/doop-root-ca.mobileconfig`](./apple/doop-root-ca.mobileconfig).
- Publication boundary: [`docs/reference/repository-scope.md`](./docs/reference/repository-scope.md).
- Publication workflow: [`docs/operations/publication-process.md`](./docs/operations/publication-process.md).

## Checks

- Markdown links: `python3 scripts/check_markdown_links.py`
- Artifact consistency: `python3 scripts/check_artifacts.py`
- Public-scope guard: `python3 scripts/public_scope_guard.py`
- Shell syntax for Linux scripts and PowerShell parser checks are also run in GitHub Actions.

## Editing Rules

- If the certificate changes, update README fingerprint/subject/validity and the Apple profile together, then run artifact checks.
- If install paths move, update README, docs index, and link checks together.
- Avoid adding environment-specific examples that reveal internal topology.
