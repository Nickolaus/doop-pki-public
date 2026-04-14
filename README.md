# doop-pki-public

Public trust-distribution and client interoperability artifacts for the `doop` internal PKI.

This repository is intentionally public-safe. It contains only the material a client needs to trust and consume the public root CA correctly, plus generic platform guidance for installing, verifying, troubleshooting, and maintaining that trust.

For the publication boundary and what must never be committed here, see:
- `SECURITY.md`
- `docs/repository-scope.md`

## Purpose
- distribute the public root CA certificate
- provide stable platform-specific trust-install artifacts
- document modern client interoperability expectations
- document verification, troubleshooting, and rotation guidance

## Who Should Use This Repo
Use this repository for managed clients that must trust internal HTTPS services:
- admin workstations
- managed servers
- managed browsers
- managed mobile devices where required
- container or node runtimes that must call internal HTTPS services

## Who Should Not Use This Repo By Default
Do not distribute this root CA broadly to:
- guest devices
- unmanaged personal devices
- most IoT devices
- public internet clients

## Canonical Public Interfaces
- `certs/doop-root-ca.crt`
- `apple/install-notes.md`
- `apple/doop-root-ca.mobileconfig`
- `android/install-notes.md`
- `linux/install-notes.md`
- `linux/install-root-ca-debian.sh`
- `linux/install-root-ca-redhat.sh`
- `windows/install-root-ca.ps1`
- `windows/install-root-ca-certutil.cmd`
- `windows/gpo-deployment-notes.md`
- `docs/client-trust-matrix.md`
- `docs/browser-interop.md`
- `docs/non-browser-clients.md`
- `docs/verification-and-troubleshooting.md`
- `docs/rotation-and-lifecycle.md`
- `docs/publication-process.md`
- `docs/public-trust-distribution.md`
- `docs/repository-scope.md`
- `SECURITY.md`

## Root Certificate
- Subject: `O=doop internal ca, CN=doop internal ca Root CA`
- SHA-256 fingerprint: `BB:9B:B1:83:DC:54:A0:90:71:9E:5C:23:EA:9F:4F:C2:62:0C:F3:B8:BA:3B:AC:A0:6A:59:E0:F6:AF:2D:CC:A0`
- Valid until: `Apr  9 11:25:56 2036 GMT`

## Direct Download

Canonical public certificate URL:

`https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt`

Canonical Apple configuration profile URL:

`https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/apple/doop-root-ca.mobileconfig`

Fetch only:

```sh
curl -fsSLo doop-root-ca.crt https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt
```

```sh
wget -qO doop-root-ca.crt https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt
```

## One-Line Install Commands

Verify the fingerprint before broad trust deployment. These commands are intended for managed clients that already meet the trust policy described in this repository.

### Debian / Ubuntu

```sh
curl -fsSL https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt | sudo tee /usr/local/share/ca-certificates/doop-root-ca.crt >/dev/null && sudo update-ca-certificates
```

### macOS

```sh
curl -fsSL https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt | sudo tee /tmp/doop-root-ca.crt >/dev/null && sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain /tmp/doop-root-ca.crt
```

### Apple Configuration Profile Download

```sh
curl -fsSLO https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/apple/doop-root-ca.mobileconfig
```

### RHEL / Fedora

```sh
curl -fsSL https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt | sudo tee /etc/pki/ca-trust/source/anchors/doop-root-ca.crt >/dev/null && sudo update-ca-trust extract
```

### Windows PowerShell

```powershell
$cert="$env:TEMP\doop-root-ca.crt"; Invoke-WebRequest https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt -OutFile $cert; Import-Certificate -FilePath $cert -CertStoreLocation Cert:\LocalMachine\Root
```

### Windows `certutil`

```cmd
powershell -NoProfile -Command "$cert='$env:TEMP\\doop-root-ca.crt'; Invoke-WebRequest https://raw.githubusercontent.com/Nickolaus/doop-pki-public/main/certs/doop-root-ca.crt -OutFile $cert" && certutil -addstore -f Root "%TEMP%\doop-root-ca.crt"
```

## Start Here
1. Read `docs/public-trust-distribution.md`.
2. Check `docs/client-trust-matrix.md` for your client class.
3. Use the platform-native install artifact or deployment path.
4. Verify the fingerprint before trusting the root.
5. If trust still fails, use `docs/browser-interop.md`, `docs/non-browser-clients.md`, and `docs/verification-and-troubleshooting.md`.

## Important Notes
- The root certificate is public by design; broad trust is not.
- Browser success does not prove that every app trusts the CA.
- Some runtimes, especially Java, Firefox, containers, and mobile apps, may need additional trust configuration beyond OS trust.
- This repository deliberately avoids publishing internal hostnames, internal IPs, private topology, or service inventory.
