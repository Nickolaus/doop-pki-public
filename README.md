# doop-pki-public

Public trust-distribution artifacts for the `doop` homelab PKI.

This repository is intentionally narrow in scope. It is safe to publish only because it contains public trust material and client-distribution helpers, not signing material.

## What belongs here
- the public root CA certificate
- client trust-install artifacts
- generic operator documentation for trust distribution
- certificate fingerprints and rotation notes

## What does not belong here
- private keys of any kind
- internal IP addresses
- private hostnames or internal topology
- server file paths
- `/etc/hosts` workarounds
- passwords, API keys, or encrypted blobs without a clear publication reason
- restore notes that reveal private infrastructure layout

## Current contents
- `certs/doop-root-ca.crt`
- `apple/doop-root-ca.mobileconfig`
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
