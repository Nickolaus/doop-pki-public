# Public Trust Distribution

This document describes how to distribute the public root CA to managed clients safely.

## Principle
The root certificate is public by design. Distributing it is safe. Trusting it should still be limited to managed clients that need to access internal HTTPS services.

## Recommended device classes
- admin macOS devices
- admin Windows devices
- admin Linux devices
- managed mobile devices when required
- container or node runtimes that must call internal HTTPS services

## Device classes to avoid by default
- guest devices
- unmanaged personal devices
- most IoT devices
- clients that do not need to reach internal HTTPS services

## Best-practice distribution model
Use platform-native trust deployment:
- Apple: configuration profile
- Windows: Intune trusted certificate profile, GPO, or script fallback
- Linux: config management or package/bootstrap script
- Android: managed-device deployment where possible; manual install only when justified

## Direct Artifact URL

Canonical public root certificate URL:

`https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt`

Canonical Apple configuration profile URL:

`https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/apple/doop-root-ca.mobileconfig`

Use that URL when a client needs a direct fetch path and cloning the repository is unnecessary.

## One-Line Install Examples

These are convenience commands for managed clients. They do not replace fingerprint verification and they should not be used as a broad trust-distribution mechanism for unmanaged devices.

### Debian / Ubuntu

```sh
curl -fsSL https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt | sudo tee /usr/local/share/ca-certificates/doop-root-ca.crt >/dev/null && sudo update-ca-certificates
```

### macOS

```sh
curl -fsSL https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt | sudo tee /tmp/doop-root-ca.crt >/dev/null && sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /tmp/doop-root-ca.crt
```

### RHEL / Fedora

```sh
curl -fsSL https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt | sudo tee /etc/pki/ca-trust/source/anchors/doop-root-ca.crt >/dev/null && sudo update-ca-trust extract
```

### Apple configuration profile download

```sh
curl -fsSLO https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/apple/doop-root-ca.mobileconfig
```

### Windows PowerShell

```powershell
$cert="$env:TEMP\doop-root-ca.crt"; Invoke-WebRequest https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt -OutFile $cert; Import-Certificate -FilePath $cert -CertStoreLocation Cert:\LocalMachine\Root
```

## Client Guidance Index
- Client trust matrix: `docs/client-trust-matrix.md`
- Browser-specific behavior: `docs/browser-interop.md`
- Non-browser runtimes: `docs/non-browser-clients.md`
- Verification and troubleshooting: `docs/verification-and-troubleshooting.md`
- Rotation and lifecycle: `docs/rotation-and-lifecycle.md`
- Publication/update process: `docs/publication-process.md`

## Rotation guidance
When the root certificate changes:
1. publish the new public certificate in `certs/`
2. regenerate platform artifacts
3. distribute the new trust anchor before any dependent service uses it
4. remove the old root only after all managed clients are migrated

## Verification guidance
Before trusting a new root on any device:
1. verify the published fingerprint out of band
2. compare it with the certificate being installed
3. only then import it into the trust store

## Operational reminder
OS trust is often necessary but not always sufficient. Some runtimes and apps maintain separate trust behavior and require additional configuration even after the system trust store is correct.
