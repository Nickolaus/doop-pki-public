# Verification and Troubleshooting

Use this guide when trust installation appears correct but HTTPS still fails.

## First Checks

1. Confirm you installed the expected root certificate.
2. Verify the SHA-256 fingerprint out of band.
3. Confirm the application is actually using the trust store you changed.
4. Inspect the server certificate chain.

## Fingerprint Verification

The published root CA fingerprint is:

`BB:9B:B1:83:DC:54:A0:90:71:9E:5C:23:EA:9F:4F:C2:62:0C:F3:B8:BA:3B:AC:A0:6A:59:E0:F6:AF:2D:CC:A0`

Compare the installed certificate against the published fingerprint before trusting it.

## Useful Commands

### OpenSSL

```sh
openssl x509 -in certs/doop-root-ca.crt -noout -subject -fingerprint -sha256 -enddate
```

```sh
openssl s_client -connect example.internal:443 -servername example.internal -showcerts
```

### `curl`

```sh
curl -v https://example.internal/
```

### Java

```sh
keytool -list -keystore "$JAVA_HOME/lib/security/cacerts" -storepass changeit
```

## How To Read Common Errors

| Symptom | Meaning |
|---|---|
| Unknown issuer | The client does not trust the root or issuing chain |
| Hostname mismatch | The certificate name does not match the URL |
| Certificate expired | The leaf, intermediate, or root is outside its validity window |
| Incomplete chain | The server did not send the expected intermediate |
| Browser works, app fails | The app is using a different trust model |
| One browser fails, others work | Browser-specific trust behavior differs |

## Decision Path

If all clients fail:
- suspect server chain, name mismatch, or wrong certificate

If OS tools fail but browser works:
- suspect the browser has a different trust path or cached session state

If browser works but Java or a container fails:
- suspect runtime-specific trust configuration

If only Firefox fails:
- suspect Firefox trust behavior before changing server certificates

## When To Reissue Certificates

Reissue the server certificate only when you have evidence of:
- hostname mismatch
- wrong SAN set
- expired certificate
- incorrect or missing chain from the server

Do not reissue just because one client type fails before verifying its trust path.

## Related Docs

- `docs/browser-interop.md`
- `docs/non-browser-clients.md`
- `docs/client-trust-matrix.md`
