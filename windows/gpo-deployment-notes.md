# Windows Deployment Notes

Use this repository's root certificate as the source artifact for Windows trust deployment.

## Preferred approaches
1. Group Policy:
   - Computer Configuration
   - Windows Settings
   - Security Settings
   - Public Key Policies
   - Trusted Root Certification Authorities
2. Intune trusted certificate profile
3. Local scripted import for unmanaged lab machines

## Source file
- `certs/doop-root-ca.crt`

## Notes
- Prefer `LocalMachine\Root` for shared/admin workstations.
- Use `CurrentUser\Root` only when machine-wide trust is not appropriate.
- Validate the certificate fingerprint before deployment.
