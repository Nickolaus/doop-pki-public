---
doc_type: runbook
canonical_for: linux_install
truth_source: doop-pki-public/certs/doop-root-ca.crt and public-safe install artifacts
last_verified: 2026-05-06
status: active
---

# Linux Install Notes

For most Linux distributions, the right approach is to install the root CA into the system trust store and then refresh the trust database.

## Recommended Paths

- Debian / Ubuntu:
  - `linux/install-root-ca-debian.sh`
- RHEL / Fedora:
  - `linux/install-root-ca-redhat.sh`
- configuration management for fleet deployment is preferred over manual per-host imports

## System Trust Model

Most Linux TLS consumers work correctly once the root CA is installed into the system trust store. Exceptions still exist:
- Java may use a separate truststore
- containers may use a different trust store than the host
- some applications may point to a custom CA bundle

## Verification

After installing the root CA:

```sh
openssl x509 -in certs/doop-root-ca.crt -noout -subject -fingerprint -sha256
```

```sh
curl -v https://example.internal/
```

If `curl` still fails:
- check whether the client uses a custom CA bundle
- check whether the server chain is complete
- compare with `openssl s_client`

## Related Docs

- `docs/reference/client-trust-matrix.md`
- `docs/reference/non-browser-clients.md`
- `docs/operations/verification-and-troubleshooting.md`
