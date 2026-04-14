# Apple Install Notes

Use the Apple configuration profile in this repository as the preferred public artifact for Apple device trust deployment.

## Preferred Deployment Paths

1. MDM trusted certificate deployment
2. Apple Configurator or equivalent managed profile deployment
3. Manual profile install only when managed deployment is not available

## Manual Install Notes

Manual installation is acceptable for small admin-only device sets, but it is not the preferred long-term path.

After installing the profile:
- confirm the profile appears in device management settings
- on platforms that require it, ensure the installed root is trusted for SSL
- test browser access to an intended internal HTTPS service

## Platform Caveat

On Apple mobile platforms, profile installation and SSL trust enablement are related but not always identical user actions. If a certificate is installed but browser trust still fails, check whether full trust for the installed root has been enabled where the platform requires that step.

## Artifact

- `apple/doop-root-ca.mobileconfig`
- direct download:
  - `https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/apple/doop-root-ca.mobileconfig`

## One-Line macOS Keychain Import

```sh
curl -fsSL https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt | sudo tee /tmp/doop-root-ca.crt >/dev/null && sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /tmp/doop-root-ca.crt
```

This path installs the root into the macOS system keychain directly. Prefer MDM or configuration profiles for managed fleets.

## Related Docs

- `docs/client-trust-matrix.md`
- `docs/verification-and-troubleshooting.md`

## References

- Apple Platform Deployment:
  - https://support.apple.com/guide/deployment/welcome/web
