# Rotation and Lifecycle

This repository publishes the public trust anchor and the client-side material needed to consume it safely.

## Root Rotation Model

When the public root changes:
1. publish the new root certificate
2. regenerate every platform-specific trust artifact derived from it
3. distribute the new trust anchor to managed clients before depending on it
4. keep the old root in place until migration is complete
5. remove the old root only after dependent clients have moved

## Intermediate Publication Guidance

If clients need intermediate certificates for chain building or troubleshooting, publish only the public intermediate certificates. Never publish intermediate private keys, signer state, or CA runtime data.

## Overlap Expectations

Plan for an overlap period where:
- the old root is still trusted on some clients
- the new root is already distributed
- dependent services are not switched until trust distribution is sufficiently complete

Do not collapse this overlap window unless you control every dependent client.

## Client Migration Ordering

Recommended order:
1. managed admin devices
2. managed servers
3. managed browsers and mobile clients
4. container and runtime images
5. any slower-moving or policy-managed endpoints

## What Must Be Updated When The Root Changes

- `certs/doop-root-ca.crt`
- any Apple configuration profile payload embedding the certificate
- fingerprint references in public docs
- Windows and Linux installation guidance if file names or paths change
- verification examples if output expectations change

## Anti-Patterns

Avoid:
- changing the root without publishing updated fingerprints
- publishing private CA material for convenience
- assuming browser trust proves runtime trust everywhere
- removing the old root before the managed fleet is migrated

## Related Docs

- `docs/publication-process.md`
- `docs/public-trust-distribution.md`
- `docs/verification-and-troubleshooting.md`
