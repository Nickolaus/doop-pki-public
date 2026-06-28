# doop-pki-public

This repository is no longer maintained as an active trust-distribution
channel.

The active trust anchor is now managed through an operator-owned private
operations repository. Do not add new clients, automation, documentation, or
deployment workflows that depend on this public repository.

## Existing Artifact

The existing public root certificate remains in this repository for consumers
that already have an explicit dependency on it:

- Artifact: `certs/doop-root-ca.crt`
- Subject: `O=doop internal ca, CN=doop internal ca Root CA`
- SHA-256 fingerprint:
  `BB:9B:B1:83:DC:54:A0:90:71:9E:5C:23:EA:9F:4F:C2:62:0C:F3:B8:BA:3B:AC:A0:6A:59:E0:F6:AF:2D:CC:A0`
- Valid until: `Apr  9 11:25:56 2036 GMT`

The root certificate is public by design. Broad trust deployment is not.

## Repository State

This repository is retained as a read-only compatibility and audit reference.
It is not the source for new public trust-distribution work, generic platform
install guidance, managed-device onboarding, or automated dependency updates.

Security boundary remains unchanged: do not publish private keys, passwords,
tokens, internal service inventory, private hostnames, local workstation paths,
private topology, or other credential-like material here.
