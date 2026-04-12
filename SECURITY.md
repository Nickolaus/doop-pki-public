# Security Policy

## Repository purpose
This repository is for public PKI trust material only.

Allowed content:
- public certificates
- trust-install artifacts
- generic client onboarding documentation

Disallowed content:
- private keys
- passwords, tokens, or API credentials
- internal IP addresses or internal topology
- local workstation paths
- server-specific filesystem paths
- recovery notes that expose private infrastructure details

## Reporting
If sensitive material is found in this repository, treat it as a publishing error:
1. remove it immediately
2. rotate any affected secret or key material
3. review commit history before publishing further changes
