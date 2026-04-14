# Publication Process

Use this process whenever the public trust material changes.

## Source Of Truth

The public repo should be updated only from reviewed public artifacts produced by the private CA workspace. Do not copy directories wholesale from the private workspace into this repo.

## Pre-Publish Review

Before adding or updating any artifact:
1. verify it contains no private key material
2. verify it contains no passwords, tokens, or credentials
3. verify it contains no internal hostnames, private suffixes, or RFC1918 addresses
4. verify it contains no local workstation paths
5. verify it belongs in a public trust-and-interoperability repo

## Publication Steps

1. update `certs/doop-root-ca.crt` if the public root changed
2. regenerate any platform artifact that embeds the certificate
3. update fingerprints and validity metadata in public docs
4. review the repository scope and security boundary
5. run the public-scope and artifact-consistency checks
6. publish only after the repository passes review and validation

## Release Notes Expectations

Release notes should mention:
- whether the public root changed
- whether platform artifacts changed
- whether install guidance changed materially
- whether verification steps changed

Release notes should not mention:
- internal service inventory
- internal topology
- private CA operations

## Sanity Checklist

- certificate parses cleanly
- fingerprint in docs matches the artifact
- embedded Apple payload matches the PEM
- platform docs point to the canonical certificate path
- no public-scope violations are present

## Related Docs

- `SECURITY.md`
- `docs/repository-scope.md`
- `docs/public-trust-distribution.md`
- `docs/rotation-and-lifecycle.md`
