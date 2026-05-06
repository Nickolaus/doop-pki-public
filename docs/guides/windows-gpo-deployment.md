---
doc_type: runbook
canonical_for: windows_gpo_deployment
truth_source: doop-pki-public/certs/doop-root-ca.crt and public-safe install artifacts
last_verified: 2026-05-06
status: active
---

# Windows Deployment Notes

Use this repository's root certificate as the source artifact for Windows trust deployment.

## Preferred approaches
1. Intune trusted certificate profile for managed devices
2. Group Policy for domain-managed devices:
   - Computer Configuration
   - Windows Settings
   - Security Settings
   - Public Key Policies
   - Trusted Root Certification Authorities
3. Local scripted import as a fallback for small unmanaged admin machines

## Source file
- `certs/doop-root-ca.crt`

## Notes
- Prefer `LocalMachine\Root` for shared/admin workstations.
- Use `CurrentUser\Root` only when machine-wide trust is not appropriate.
- Validate the certificate fingerprint before deployment.
- Browser success usually follows machine trust on Windows, but Firefox and Java should still be treated as separate client classes when troubleshooting.

## Validation

Recommended checks:
- verify the certificate is present in `certlm.msc` under Trusted Root Certification Authorities
- verify with `certutil -store Root`
- test browser access to an intended internal HTTPS service

## Related Docs

- `docs/reference/client-trust-matrix.md`
- `docs/reference/browser-interop.md`
- `docs/operations/verification-and-troubleshooting.md`
