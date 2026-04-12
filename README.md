# doop-pki-public

Public trust-distribution artifacts for the `doop` homelab PKI.

This repository contains only public trust material and client-distribution helpers.

For the publication boundary and what must never be committed here, see:
- `SECURITY.md`
- `docs/repository-scope.md`

## Purpose
- distribute the public root CA certificate
- provide per-platform trust-install artifacts
- document safe client trust rollout

## Current contents
- `certs/doop-root-ca.crt`
- `apple/doop-root-ca.mobileconfig`
- `android/install-notes.md`
- `linux/install-root-ca-debian.sh`
- `linux/install-root-ca-redhat.sh`
- `windows/install-root-ca.ps1`
- `windows/install-root-ca-certutil.cmd`
- `windows/gpo-deployment-notes.md`
- `docs/public-trust-distribution.md`
- `docs/repository-scope.md`
- `SECURITY.md`

## Root certificate
- Subject: `O=doop internal ca, CN=doop internal ca Root CA`
- SHA-256 fingerprint: `BB:9B:B1:83:DC:54:A0:90:71:9E:5C:23:EA:9F:4F:C2:62:0C:F3:B8:BA:3B:AC:A0:6A:59:E0:F6:AF:2D:CC:A0`

## Usage
Only import this root CA on managed clients that must trust internal HTTPS services.

Typical targets:
- admin laptops and desktops
- admin mobile devices if they need internal HTTPS access
- managed Linux servers that call internal HTTPS services

Do not import it broadly onto guest or unmanaged devices.
